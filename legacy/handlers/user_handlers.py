# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import database as db
from translations import TRANSLATIONS
from shared import (
    DEFAULT_MODEL, _, create_roles_selection_keyboard, 
    create_model_selection_keyboard, create_options_keyboard, 
    create_language_selection_keyboard, SMART_ASSISTANT_ROLE, 
    get_user_lang
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command. Triggers a full reset and language selection."""
    chat_id = update.effective_chat.id
    db.full_user_reset(chat_id)
    await update.message.reply_text(
        TRANSLATIONS['ru']['welcome_choose_lang'],
        reply_markup=create_language_selection_keyboard()
    )

async def show_model_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the model selection menu."""
    chat_id = update.effective_chat.id
    settings = db.get_user_settings(chat_id, DEFAULT_MODEL, "")
    await update.message.reply_text(
        _(chat_id, "model_menu_title", current_model=f"`{settings['model']}`"),
        reply_markup=create_model_selection_keyboard(),
        parse_mode='Markdown'
    )

async def show_options_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the chat options menu."""
    await update.message.reply_text(
        _(update.effective_chat.id, "options_menu_title"),
        reply_markup=create_options_keyboard(update.effective_chat.id)
    )
