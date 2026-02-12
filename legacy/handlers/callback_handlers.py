### Файл: handlers/callback_handlers.py
# -*- coding: utf-8 -*-
import logging
from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import database as db
from shared import AVAILABLE_ROLES, DEFAULT_MODEL, _, create_options_keyboard, create_roles_selection_keyboard, get_user_lang, SMART_ASSISTANT_ROLE
# Импортируем админские функции для меню
from handlers.admin_handlers import create_user_selection_keyboard, show_user_info_details

logger = logging.getLogger(__name__)

# --- Individual handler functions for each button type ---

async def _handle_lang_selection(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    lang = query.data.split('_', 1)[1]
    chat_id = query.message.chat_id
    user = query.from_user
    new_settings = { 'chat_id': chat_id, 'language': lang, 'system_prompt': SMART_ASSISTANT_ROLE[lang], 'model': DEFAULT_MODEL, 'memory_enabled': True, 'is_banned': False, 'state': None, 'first_name': user.first_name, 'username': user.username }
    db.save_user_settings(chat_id, new_settings)
    base_welcome_text = _(chat_id, "start_after_restart", user_name=(user.first_name or user.username))
    parts = base_welcome_text.split('\n\n', 1)
    greeting_line, rest_of_text = parts[0], parts[1] if len(parts) > 1 else ""
    full_welcome_text = f"{greeting_line} (UserID: `{chat_id}`)\n\n{rest_of_text}"
    await query.edit_message_text(full_welcome_text, reply_markup=create_roles_selection_keyboard(chat_id), parse_mode=ParseMode.MARKDOWN)

async def _handle_model_selection(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    settings['model'] = query.data.split("_", 1)[1]
    db.save_user_settings(query.message.chat_id, settings)
    await query.edit_message_text(_(query.message.chat_id, "model_changed", model_name=f"`{settings['model']}`"), parse_mode='Markdown')

async def _handle_toggle_memory(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    settings['memory_enabled'] = not settings['memory_enabled']
    db.save_user_settings(query.message.chat_id, settings)
    await query.edit_message_reply_markup(reply_markup=create_options_keyboard(query.message.chat_id))

async def _handle_show_roles_menu(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    await query.edit_message_text(_(query.message.chat_id, "roles_menu_title"), reply_markup=create_roles_selection_keyboard(query.message.chat_id))

async def _handle_role_selection(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    lang = get_user_lang(query.message.chat_id)
    role_key = query.data.split("_", 1)[1]
    settings['system_prompt'] = AVAILABLE_ROLES[lang][role_key]
    db.save_user_settings(query.message.chat_id, settings)
    await query.edit_message_text(_(query.message.chat_id, "role_chosen"), reply_markup=None)

async def _handle_role_skip(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    lang = get_user_lang(query.message.chat_id)
    settings['system_prompt'] = SMART_ASSISTANT_ROLE[lang]
    db.save_user_settings(query.message.chat_id, settings)
    await query.edit_message_text(_(query.message.chat_id, "role_skipped"), reply_markup=None)

async def _handle_set_custom_prompt(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    db.set_user_state(query.message.chat_id, 'awaiting_system_prompt')
    await query.message.reply_text(_(query.message.chat_id, "prompt_for_custom_role"))
    await query.delete_message()

async def _handle_back_to_options(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    await query.edit_message_text(_(query.message.chat_id, "options_menu_title"), reply_markup=create_options_keyboard(query.message.chat_id))

async def _handle_show_status(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    chat_id = query.message.chat_id
    memory = _(chat_id, 'btn_memory_on') if settings['memory_enabled'] else _(chat_id, 'btn_memory_off')
    await query.edit_message_text(_(chat_id, "current_settings_title", model=f"`{settings['model']}`", memory=memory, prompt=f"`{settings['system_prompt']}`"), reply_markup=create_options_keyboard(chat_id), parse_mode='Markdown')

async def _handle_close_options(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    await query.delete_message()
    
# Handlers for the /userinfo menu
async def _handle_userinfo_page(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    """Handles pagination for the user list."""
    page = int(query.data.split('_')[-1])
    await query.edit_message_text(
        "👤 *Выберите пользователя для просмотра информации:*",
        reply_markup=create_user_selection_keyboard(page=page),
        parse_mode=ParseMode.MARKDOWN
    )

async def _handle_userinfo_selection(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, settings: dict):
    """Handles the selection of a user from the list."""
    user_id = int(query.data.split('_')[-1])
    await show_user_info_details(query, context, user_id)

# Dispatcher dictionary
CALLBACK_HANDLERS = {
    "lang_": _handle_lang_selection,
    "model_": _handle_model_selection,
    "toggle_memory": _handle_toggle_memory,
    "show_roles_menu": _handle_show_roles_menu,
    "role_": _handle_role_selection,
    "role_skip": _handle_role_skip,
    "set_custom_prompt": _handle_set_custom_prompt,
    "back_to_options": _handle_back_to_options,
    "show_status": _handle_show_status,
    "close_options": _handle_close_options,
    "userinfo_page_": _handle_userinfo_page,
    "userinfo_": _handle_userinfo_selection,
}

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The main handler for all button presses."""
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    
    settings = db.get_user_settings(chat_id, DEFAULT_MODEL, "")
    
    for prefix, handler_func in CALLBACK_HANDLERS.items():
        if query.data.startswith(prefix):
            await handler_func(query, context, settings)
            return
            
    logger.warning(f"No handler found for callback_data: {query.data}")
