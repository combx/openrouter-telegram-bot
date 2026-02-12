from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from src.services.user_service import get_or_create_user, log_error, increment_usage, set_user_state, update_user_model
from src.database import get_db
from src.services.openrouter import OpenRouterService
from src.config import Config
import json

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
            # Perform search (mockup for now as we don't have a real search index of 100s models without API call)
            # Actually OpenRouter API list models. We can filter them.
            status = await update.message.reply_text("🔎 Searching...")
            
            api_key = user.custom_api_key or Config.OPENROUTER_API_KEY
            service = OpenRouterService(api_key=api_key)
            
            # Simple search logic
            # In a real app, we should cache the model list
            try:
                # We can't easily search via API without fetching all. 
                # Let's assume the user wants to set the model directly or we show top matches from a hardcoded list for now
                # Or better: just set the model if it looks like a model ID, or search in a hardcoded list.
                # Since I don't have the full list, I'll allow setting it if it contains "/"
                
                if "/" in text:
                    await update_user_model(session, user_id, text)
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"✅ Model set to `{text}`", parse_mode="Markdown")
                    await set_user_state(session, user_id, None)
                else:
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text="❌ Invalid model format. Please enter `vendor/model_name` or use the menu.")
                    
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
        
        messages = [
            {"role": "system", "content": f"You are a {user.current_role}."},
            {"role": "user", "content": text}
        ]
        
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
            await increment_usage(session, user_id)

        except Exception as e:
            await log_error(session, user_id, str(e), "")
            error_text = f"⚠️ Error: {str(e)}"
            if full_response:
                error_text += "\n\nPartial response received."
                await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=full_response)
                await update.message.reply_text(error_text)
            else:
                await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=error_text)
