from telegram import Update
from telegram.ext import ContextTypes
from src.services.user_service import get_or_create_user
from src.database import get_db
from src.utils.keyboard import Keyboards
from src.config import Config

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    async for session in get_db():
        db_user = await get_or_create_user(
            session, 
            telegram_id=user.id, 
            username=user.username, 
            full_name=user.full_name
        )
        # Check ban status
        if db_user.is_banned:
            await update.message.reply_text("🚫 You are banned from using this bot.")
            return

        is_admin = (user.id == Config.ADMIN_ID)
        
        await update.message.reply_text(
            f"Hello, {user.first_name}!\n"
            f"Current Model: `{db_user.current_model}`\n"
            f"Select an option below:",
            reply_markup=Keyboards.main_menu(is_admin=is_admin),
            parse_mode="Markdown"
        )
