from telegram import Update, constants
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from src.services.user_service import get_or_create_user, log_error, increment_usage, set_user_state, update_user_model, set_custom_key
from src.database import get_db
from src.services.openrouter import OpenRouterService
from src.config import Config
from src.utils.markdown import MarkdownCleaner
import json
import asyncio

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    
    async for session in get_db():
        user = await get_or_create_user(session, user_id, update.effective_user.username, update.effective_user.full_name)
        
        if user.is_banned:
            return

        # Route to specific handlers based on state
        if user.state == "SEARCH_MODE":
            await _handle_search_mode(update, context, user, session)
        elif user.state == "SET_CUSTOM_KEY":
            await _handle_settings_mode(update, context, user, session)
        else:
            await _handle_chat(update, context, user, session)

async def _handle_search_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, user, session):
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    user_id = user.id

    # Heuristic: If text is long or looks like a question, treat as chat
    if len(text) > 50 or "?" in text or " " in text and len(text.split()) > 5:
        await set_user_state(session, user_id, None)
        await update.message.reply_text("🔄 Search cancelled. Sending as message...")
        # Update local object
        user.state = None
        # Fallback to chat
        await _handle_chat(update, context, user, session)
        return

    status = await update.message.reply_text("🔎 Searching...")
    api_key = user.custom_api_key or Config.OPENROUTER_API_KEY
    service = OpenRouterService(api_key=api_key)
    
    try:
        if "/" in text and " " not in text:
            await update_user_model(session, user_id, text)
            await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"✅ Model set to `{text}`", parse_mode="Markdown")
            await set_user_state(session, user_id, None)
        else:
            results = await service.search_models(text)
            if not results:
                await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text="❌ No models found. Try a different query.")
            else:
                keyboard = []
                for model in results[:5]:
                    name = model.get('name', model.get('id'))
                    if len(name) > 30: name = name[:27] + "..."
                    keyboard.append([InlineKeyboardButton(name, callback_data=f"set_model_{model.get('id')}")])
                
                keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_model")])
                
                await context.bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=status.message_id, 
                    text=f"🔎 Found {len(results)} models for `{text}`:", 
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
                await set_user_state(session, user_id, None)
            
    except Exception as e:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"Error: {e}")

async def _handle_settings_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, user, session):
    text = update.message.text.strip()
    user_id = user.id

    if text == "-":
        await set_custom_key(session, user_id, None)
        await update.message.reply_text("✅ Custom key removed. Using shared key.")
    else:
        if not text.isascii():
            await update.message.reply_text("❌ Invalid API Key. Latin characters only.")
            return

        await set_custom_key(session, user_id, text)
        await update.message.reply_text("✅ Custom key saved!")
    
    await set_user_state(session, user_id, None)

async def _handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, user, session):
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    user_id = user.id
    
    api_key = user.custom_api_key or Config.OPENROUTER_API_KEY
    service = OpenRouterService(api_key=api_key)
    
    status_msg = await update.message.reply_text("⏳ Thinking...")
    
    # Load History
    try:
        history = json.loads(user.context_history) if user.context_history else []
        if not isinstance(history, list): history = []
    except:
        history = []
        
    history.append({"role": "user", "content": text})
    messages = [{"role": "system", "content": f"You are a {user.current_role}."}] + history
    
    full_response = ""
    last_edit_time = 0
    stream_stopped = False
    
    try:
        async for chunk in service.stream_chat(user.current_model, messages):
            full_response += chunk
            
            # Streaming Logic (Limit to 4000 chars to avoid crash)
            if len(full_response) > 4000:
                if not stream_stopped:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=status_msg.message_id,
                        text=MarkdownCleaner.clean_bot_response(full_response[:4000] + "...\n(Continuing...)"),
                        parse_mode="MarkdownV2"
                    )
                    stream_stopped = True
                continue

            # Update every 1.5s
            import time
            current_time = time.time()
            if current_time - last_edit_time > 1.5:
                try:
                    cleaned_text = MarkdownCleaner.clean_bot_response(full_response + "...")
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=status_msg.message_id,
                        text=cleaned_text,
                        parse_mode="MarkdownV2"
                    )
                    last_edit_time = current_time
                except BadRequest:
                    pass

        # Final Send
        if len(full_response) <= 4000:
            cleaned_text = MarkdownCleaner.clean_bot_response(full_response)
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text=cleaned_text,
                parse_mode="MarkdownV2"
            )
        else:
            # Long message: Split and send
            # First, update the status message with the first chunk
            await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
            
            # Simple chunking by 4096
            for i in range(0, len(full_response), 4096):
                chunk_text = full_response[i:i+4096]
                cleaned_chunk = MarkdownCleaner.clean_bot_response(chunk_text)
                await update.message.reply_text(cleaned_chunk, parse_mode="MarkdownV2")
        
        # Save History
        history.append({"role": "assistant", "content": full_response})
        if len(history) > 20:
            history = history[-20:]
            
        from sqlalchemy import update as sa_update
        from src.database.models import User
        stmt = sa_update(User).where(User.id == user_id).values(context_history=json.dumps(history))
        await session.execute(stmt)
        await session.commit()
        await increment_usage(session, user_id)

    except Exception as e:
        await log_error(session, user_id, str(e), "")
        error_str = str(e)
        
        if "429" in error_str or "rate-limited" in error_str.lower():
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Change Model", callback_data="menu_model")]])
            text = f"⚠️ *Model Overloaded*\n\nModel `{user.current_model}` is busy\\."
            await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=MarkdownCleaner.escape(text), reply_markup=kb, parse_mode="MarkdownV2")
        else:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=f"⚠️ Error: {error_str}")
