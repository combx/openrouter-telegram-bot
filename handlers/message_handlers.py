# -*- coding: utf-8 -*-
import logging
import asyncio
import traceback
from telegram import Update, Message, User
from telegram.ext import ContextTypes
from telegram.error import BadRequest
import database as db
from shared import MODEL_ID_TO_NAME, DEFAULT_MODEL, _, get_user_lang, SMART_ASSISTANT_ROLE

logger = logging.getLogger(__name__)

async def notify_admin_on_error(bot, error: Exception, user: User, message_text: str, traceback_str: str):
    from shared import ADMIN_ID
    if ADMIN_ID == 0: return
    user_info = f"UserID: `{user.id}`\nName: {user.first_name}"
    if user.username: user_info += f"\nUsername: @{user.username}"
    error_message = (f"🚨 *An unexpected error occurred!*\n\n"
                     f"👤 *User:*\n{user_info}\n\n"
                     f"📝 *User Message:*\n`{message_text}`\n\n"
                     f"🔍 *Error:*\n`{type(error).__name__}: {error}`\n\n"
                     f"```\n{traceback_str[:3000]}\n```")
    try: await bot.send_message(chat_id=ADMIN_ID, text=error_message, parse_mode='Markdown')
    except Exception as e: logger.error(f"Failed to send error notification to admin: {e}")

async def generate_response_stream(message_to_reply: Message, context: ContextTypes.DEFAULT_TYPE, client) -> tuple[str, int] | None:
    chat_id = message_to_reply.chat_id
    settings = db.get_user_settings(chat_id, DEFAULT_MODEL, "")
    model_id, model_name = settings['model'], MODEL_ID_TO_NAME.get(settings['model'], settings['model'])
    placeholder_message = await message_to_reply.reply_text(_(chat_id, "thinking_indicator", model_name=model_name))
    history, messages_to_send = db.get_user_history(chat_id), [{"role": "system", "content": settings['system_prompt']}]
    if settings['memory_enabled']:
        for pair in history: messages_to_send.extend([{"role": "user", "content": pair["user_message_text"]}, {"role": "assistant", "content": pair["bot_response_text"]}])
    messages_to_send.append({"role": "user", "content": message_to_reply.text})
    full_response, current_message, current_message_text = "", placeholder_message, ""
    TELEGRAM_MSG_LIMIT = 4000
    try:
        loop = asyncio.get_running_loop()
        stream = await loop.run_in_executor(None, lambda: client.chat.completions.create(model=model_id, messages=messages_to_send, stream=True))
        last_edit_time = 0; edit_interval = 0.7
        for chunk in stream:
            chunk_content = chunk.choices[0].delta.content
            if not chunk_content: continue
            full_response += chunk_content; current_message_text += chunk_content
            if len(current_message_text) > TELEGRAM_MSG_LIMIT:
                await context.bot.edit_message_text(current_message_text, chat_id=current_message.chat_id, message_id=current_message.message_id)
                current_message = await current_message.reply_text("..."); current_message_text = ""; last_edit_time = 0
            current_time = asyncio.get_event_loop().time()
            if current_time - last_edit_time > edit_interval and current_message_text:
                try:
                    await context.bot.edit_message_text(current_message_text, chat_id=current_message.chat_id, message_id=current_message.message_id)
                    last_edit_time = current_time
                except BadRequest as e:
                    if "Message is not modified" in str(e): pass
                    elif "Message_too_long" in str(e): logger.warning("Caught Message_too_long, ignoring.")
                    else: logger.warning(f"BadRequest on edit: {e}")
        final_text = current_message_text or _(chat_id, 'empty_response')
        if final_text != placeholder_message.text:
            await context.bot.edit_message_text(final_text, chat_id=current_message.chat_id, message_id=current_message.message_id)
        if full_response: return full_response, placeholder_message.message_id
    except Exception as e:
        logger.error(f"Error during API stream: {traceback.format_exc()}")
        error_text, friendly_message = str(e).lower(), _(chat_id, 'error_unexpected')
        if "rate limit" in error_text or "429" in error_text: friendly_message = _(chat_id, 'error_rate_limit')
        elif "not found" in error_text or "404" in error_text: friendly_message = _(chat_id, 'error_not_found')
        elif "authentication" in error_text or "401" in error_text: friendly_message = _(chat_id, 'error_auth')
        else: await notify_admin_on_error(context.bot, e, message_to_reply.from_user, message_to_reply.text, traceback.format_exc())
        await context.bot.edit_message_text(friendly_message, chat_id=placeholder_message.chat_id, message_id=placeholder_message.message_id)
        return None

async def process_user_message(message: Message, context: ContextTypes.DEFAULT_TYPE, client, is_edited: bool = False) -> None:
    chat_id, new_text, user = message.chat_id, message.text, message.from_user
    settings = db.get_user_settings(chat_id, DEFAULT_MODEL, "")
    if settings.get('is_banned'): logger.info(f"Ignored message from banned user {chat_id}"); return
    if settings.get('first_name') != user.first_name or settings.get('username') != user.username:
        settings['first_name'], settings['username'] = user.first_name, user.username
        db.save_user_settings(chat_id, settings)
        logger.info(f"Updated user info for {chat_id}")
    if settings.get('state') == 'awaiting_system_prompt':
        if new_text == "-":
            settings['system_prompt'] = SMART_ASSISTANT_ROLE[get_user_lang(chat_id)]
            await message.reply_text(_(chat_id, "role_reset"))
        else:
            settings['system_prompt'] = new_text
            await message.reply_text(_(chat_id, "role_set_custom"))
        settings['state'] = None; db.save_user_settings(chat_id, settings)
        return
    if is_edited:
        history = db.get_user_history(chat_id, limit=1)
        if history and history[0]["user_message_id"] == message.message_id:
            logger.info(f"Last message is being edited. Deleting old response.")
            try: await context.bot.delete_message(chat_id=chat_id, message_id=history[0]["bot_response_id"])
            except BadRequest as e: logger.warning(f"Could not delete old bot message: {e}")
            db.delete_last_history_pair(chat_id)
    response_data = await generate_response_stream(message, context, client)
    if response_data:
        bot_response_text, bot_response_id = response_data
        if settings['memory_enabled']:
            new_pair = {"user_message_id": message.message_id, "user_message_text": new_text, "bot_response_id": bot_response_id, "bot_response_text": bot_response_text}
            db.add_to_history(chat_id, new_pair)
