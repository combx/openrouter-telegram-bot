from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from src.services.user_service import get_or_create_user, log_error, increment_usage, set_user_state, update_user_model
from src.database import get_db
from src.services.openrouter import OpenRouterService
from src.config import Config
import json

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    async for session in get_db():
        user = await get_or_create_user(session, user_id, update.effective_user.username, update.effective_user.full_name)
        
        if user.is_banned:
            return

        # Handle States
        if user.state == "SEARCH_MODE":
            status = await update.message.reply_text("🔎 Searching...")
            
            api_key = user.custom_api_key or Config.OPENROUTER_API_KEY
            service = OpenRouterService(api_key=api_key)
            
            try:
                # If looks like a direct ID (has / and no spaces), try to set it
                if "/" in text and " " not in text:
                    await update_user_model(session, user_id, text)
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"✅ Model set to `{text}`", parse_mode="Markdown")
                    await set_user_state(session, user_id, None)
                else:
                    # Perform search
                    results = await service.search_models(text)
                    
                    if not results:
                        await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text="❌ No models found. Try a different query.")
                    else:
                        keyboard = []
                        for model in results[:5]:
                            name = model.get('name', model.get('id'))
                            # Shorten name
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
            
            return

        elif user.state == "SET_CUSTOM_KEY":
            if text == "-":
                await set_custom_key(session, user_id, None)
                await update.message.reply_text("✅ Custom key removed. Using shared key.")
            else:
                await set_custom_key(session, user_id, text)
                await update.message.reply_text("✅ Custom key saved!")
            
            await set_user_state(session, user_id, None)
            return

        # Normal Chat Flow
        api_key = user.custom_api_key or Config.OPENROUTER_API_KEY
        service = OpenRouterService(api_key=api_key)
        
        status_msg = await update.message.reply_text("⏳ Thinking...")
        
        # Load History
        try:
            history = json.loads(user.context_history) if user.context_history else []
            if not isinstance(history, list): history = []
        except:
            history = []
            
        # Append User Message
        history.append({"role": "user", "content": text})
        
        # Prepare Messages for API (System + History)
        messages = [{"role": "system", "content": f"You are a {user.current_role}."}] + history
        
        full_response = ""
        last_edit_time = 0
        
        try:
            async for chunk in service.stream_chat(user.current_model, messages):
                full_response += chunk
                import time
                current_time = time.time()
                if current_time - last_edit_time > 1.5:
                    try:
                        await context.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=status_msg.message_id,
                            text=full_response + "..."
                        )
                        last_edit_time = current_time
                    except BadRequest:
                        pass

            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text=full_response
            )
            
            # Save Assistant Response to History
            history.append({"role": "assistant", "content": full_response})
            
            # Trim History (Keep last 20 messages to save context/tokens)
            if len(history) > 20:
                history = history[-20:]
                
            user.context_history = json.dumps(history)
            await increment_usage(session, user_id) # formatting helper that commits
            # Note: increment_usage commits, so our context_history change is saved too IF it's attached to session.
            # But increment_usage executes a specific UPDATE statement, it might NOT commit the user object changes if using ORM + explicit update.
            # Let's verify increment_usage implementation. 
            # It uses update(User)... so it might NOT save 'user.context_history' if we just set the attribute.
            # We should explicitly update the context history or ensure it's saved.
            
            # Safe update for history
            from sqlalchemy import update as sa_update
            from src.database.models import User
            stmt = sa_update(User).where(User.id == user_id).values(context_history=json.dumps(history))
            await session.execute(stmt)
            await session.commit()

        except Exception as e:
            await log_error(session, user_id, str(e), "")
            error_str = str(e)
            
            # Smart Error Handling
            if "429" in error_str or "rate-limited" in error_str.lower():
                kb = InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Change Model", callback_data="menu_model")]])
                friendly_text = (
                    f"⚠️ **Model Overloaded**\n\n"
                    f"The model `{user.current_model}` is currently rate-limited by the provider.\n"
                    f"Please try again later or choose a different model."
                )
                if not full_response:
                    await context.bot.edit_message_text(
                        chat_id=chat_id, 
                        message_id=status_msg.message_id, 
                        text=friendly_text,
                        reply_markup=kb,
                        parse_mode="Markdown"
                    )
                else:
                     await update.message.reply_text(friendly_text, reply_markup=kb, parse_mode="Markdown")
            
            else:
                # Generic Error
                error_text = f"⚠️ Error: {error_str}"
                if full_response:
                    error_text += "\n\nPartial response received."
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=full_response)
                    await update.message.reply_text(error_text)
                else:
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=error_text)

