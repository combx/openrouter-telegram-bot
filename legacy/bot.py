# -*- coding: utf-8 -*-
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update, BotCommand, BotCommandScopeChat
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Import local modules
import database as db
from handlers.user_handlers import start, show_model_menu, show_options_menu
from handlers.admin_handlers import show_stats, ping, user_info, ban_user, unban_user, list_users
from handlers.callback_handlers import button_callback_handler
from handlers.message_handlers import process_user_message

# --- SETUP ---
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file.")

# --- BOT LAUNCH ---
async def post_init(application: Application) -> None:
    """Sets bot commands for users and the admin after initialization."""
    user_commands = [
        BotCommand("start", "🚀 Restart / Change Language"),
        BotCommand("model", "🧠 Change Model"),
        BotCommand("options", "⚙️ Settings"),
    ]
    admin_commands = user_commands + [
        BotCommand("stats", "📊 Stats"),
        BotCommand("ping", "📡 Ping"),
        BotCommand("userinfo", "ℹ️ User Info"),
        BotCommand("ban", "🚫 Ban User"),
        BotCommand("unban", "✅ Unban User"),
        BotCommand("listusers", "👥 List Users"),
    ]
    
    await application.bot.set_my_commands(user_commands)
    
    admin_id = int(os.getenv("ADMIN_ID", "0"))
    if admin_id != 0:
        await application.bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin_id))
        try:
            await application.bot.send_message(chat_id=admin_id, text="✅ Bot started/restarted. Notification system is active.")
        except Exception as e:
            logger.error(f"Failed to send start notification to admin: {e}")

def main() -> None:
    """Initializes and runs the bot."""
    db.init_db()

    openai_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    
    builder = Application.builder().token(TELEGRAM_TOKEN)
    builder.post_init(post_init)
    application = builder.build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("model", show_model_menu))
    application.add_handler(CommandHandler("options", show_options_menu))
    
    # Register admin command handlers
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("userinfo", user_info))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))
    application.add_handler(CommandHandler("listusers", list_users))
    
    # Register other handlers
    application.add_handler(CallbackQueryHandler(button_callback_handler))
    
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.UpdateType.EDITED_MESSAGE,
        lambda u, c: process_user_message(u.message, c, openai_client, is_edited=False)
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.UpdateType.EDITED_MESSAGE,
        lambda u, c: process_user_message(u.edited_message, c, openai_client, is_edited=True)
    ))
    
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
