### Файл: handlers/admin_handlers.py
# -*- coding: utf-8 -*-
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import database as db
from shared import admin_only, DEFAULT_MODEL, _

# <<< НОВОЕ: Функция для создания клавиатуры со списком пользователей >>>
def create_user_selection_keyboard(page: int = 0, users_per_page: int = 5) -> InlineKeyboardMarkup:
    """Creates a paginated keyboard of users for selection."""
    all_users = db.get_all_users_with_activity()
    
    start_index = page * users_per_page
    end_index = start_index + users_per_page
    
    users_on_page = all_users[start_index:end_index]
    
    keyboard = []
    for user in users_on_page:
        name = user['first_name'] or "No Name"
        username = f"(@{user['username']})" if user['username'] else ""
        button_text = f"{name} {username}".strip()
        # callback_data будет содержать префикс и ID пользователя
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"userinfo_{user['chat_id']}")])
        
    # Навигационные кнопки
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("<< Назад", callback_data=f"userinfo_page_{page - 1}"))
    if end_index < len(all_users):
        nav_buttons.append(InlineKeyboardButton("Далее >>", callback_data=f"userinfo_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
        
    return InlineKeyboardMarkup(keyboard)

@admin_only
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (код этой функции без изменений)
    stats = db.get_bot_stats()
    stats_text = (f"📊 *Bot Statistics*\n\n"
                  f"👥 *Total Users:* {stats['total_users']}\n"
                  f"📨 *Total Messages (pairs):* {stats['total_messages']}\n"
                  f"📈 *Messages Today:* {stats['today_messages']}\n"
                  f"🏃 *Active Users Today:* {stats['today_active_users']}")
    await update.message.reply_text(stats_text, parse_mode='Markdown')

@admin_only
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (код этой функции без изменений)
    await update.message.reply_text("✅ Pong! I'm alive and ready to serve.")

# <<< ИЗМЕНЕНИЕ: user_info теперь запускает меню выбора >>>
@admin_only
async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows a paginated list of users to select from for getting info."""
    # Если передан ID, показываем инфо сразу (для обратной совместимости)
    if context.args:
        try:
            user_id = int(context.args[0])
            await show_user_info_details(update, context, user_id)
            return
        except (ValueError, IndexError):
            await update.message.reply_text("Неверный формат ID.")
            return

    # Если ID не передан, показываем меню
    await update.message.reply_text(
        "👤 *Выберите пользователя для просмотра информации:*",
        reply_markup=create_user_selection_keyboard(page=0),
        parse_mode=ParseMode.MARKDOWN
    )

# <<< НОВОЕ: Отдельная функция для отображения деталей, которая будет вызываться кнопкой >>>
async def show_user_info_details(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Fetches and displays detailed information for a given user_id."""
    try:
        settings = db.get_user_settings(user_id, DEFAULT_MODEL, "")
        if not settings.get('language'): 
            await update.message.reply_text(f"Пользователь с ID {user_id} не найден в БД."); return
        
        history = db.get_user_history(user_id, limit=3)
        ban_status = "❌ Забанен" if settings.get('is_banned') else "✅ Активен"
        info_text = (f"👤 *Инфо о пользователе {user_id}*\n\n*Статус:* {ban_status}\n*Имя:* {settings.get('first_name')}\n"
                     f"*Юзернейм:* @{settings.get('username')}\n*Язык:* {settings.get('language')}\n"
                     f"*Модель:* `{settings['model']}`\n*Память:* {'Вкл' if settings['memory_enabled'] else 'Выкл'}\n"
                     f"*Роль:* `{settings['system_prompt'][:100]}...`\n\n*Последние 3 сообщения:*")
        
        # Если команда вызвана сообщением, отвечаем на него. Если кнопкой - редактируем.
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(info_text, parse_mode='Markdown')
        else: # update is actually a CallbackQuery
            await update.edit_message_text(info_text, parse_mode='Markdown')

        if history:
            for pair in history: 
                # Отправляем отдельными сообщениями, чтобы не превысить лимит
                if isinstance(update, Update) and update.message:
                    await update.message.reply_text(f"*{'Юзер'}:* {pair['user_message_text']}\n*{'Бот'}:* {pair['bot_response_text']}", parse_mode='Markdown')
                else: # query.message
                    await update.message.reply_text(f"*{'Юзер'}:* {pair['user_message_text']}\n*{'Бот'}:* {pair['bot_response_text']}", parse_mode='Markdown')
        else:
            if isinstance(update, Update) and update.message:
                await update.message.reply_text("_История сообщений пуста._")
            else:
                await update.message.reply_text("_История сообщений пуста._")
    except Exception as e:
        error_message = f"Не удалось получить инфо: {e}"
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(error_message)
        else:
            await update.edit_message_text(error_message)


@admin_only
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (код этой функции без изменений)
    pass

@admin_only
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (код этой функции без изменений)
    pass

@admin_only
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (код этой функции без изменений)
    pass