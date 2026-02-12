import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from src.config import Config
from src.database.core import init_db
from src.handlers.command import start_command
from src.handlers.message import message_handler
from src.handlers.callback import callback_handler
from src.handlers.admin import admin_stats, admin_ban_user, admin_unban_user, admin_logs

# Initialize DB on startup
async def post_init(app):
    await init_db()
    print("Database initialized.")

def main():
    # Helper to check config
    try:
        Config.check_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    app = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).post_init(post_init).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    
    # Admin Commands
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("ban", admin_ban_user))
    app.add_handler(CommandHandler("unban", admin_unban_user))
    app.add_handler(CommandHandler("logs", admin_logs))
    
    # Callbacks (Menu navigation)
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    # Messages (Chat & Text Input)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
