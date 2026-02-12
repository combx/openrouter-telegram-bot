# -*- coding: utf-8 -*-

# All user-facing strings for different languages are stored here.
TRANSLATIONS = {
    'ru': {
        "welcome_choose_lang": "Пожалуйста, выберите ваш язык. / Please select your language.",
        "welcome_after_lang": "Язык установлен!\n\nЯ готов к работе. История чата очищена.\n\n"
                              "Для начала, выбери роль для бота или пропусти этот шаг, чтобы использовать стандартного ассистента.",
        "start_after_restart": "Привет, {user_name}!\n\nЯ готов к работе. История чата очищена.\n\n"
                               "Для начала, выбери роль для бота или пропусти этот шаг.",
        "role_chosen": "✅ Роль успешно изменена! Теперь просто отправь мне сообщение.",
        "role_skipped": "Хорошо, используем стандартного ассистента. Теперь просто отправь мне сообщение.",
        "role_reset": "✅ Роль сброшена на стандартную.",
        "role_set_custom": "✅ Новая роль установлена!",
        "prompt_for_custom_role": "Пожалуйста, отправь мне новый текст для роли. Для сброса на стандартную роль отправь `-`.",
        "btn_skip_role": "➡️ Пропустить",
        "btn_set_custom_role": "✏️ Ввести свою роль",
        "btn_back_to_settings": "⬅️ Назад к настройкам",
        "btn_memory_on": "✅ Память вкл.",
        "btn_memory_off": "❌ Память выкл.",
        "btn_choose_role": "🎭 Выбрать роль",
        "btn_show_settings": "ℹ️ Показать настройки",
        "btn_back_to_chat": "⬅️ Назад к чату",
        "options_menu_title": "⚙️ Настройки чата:",
        "roles_menu_title": "Выберите готовую роль или введите свою:",
        "model_menu_title": "Текущая модель: `{current_model}`\n\nВыберите новую:",
        "model_changed": "✅ Модель изменена на `{model_name}`.",
        "current_settings_title": "Текущие настройки:\n\n"
                                  "🧠 *Модель:* `{model}`\n"
                                  "💾 *Память:* {memory}\n"
                                  "🎭 *Роль:* \n`{prompt}`",
        "admin_no_permission": "⛔️ У вас нет прав для выполнения этой команды.",
        "thinking_indicator": "🧠 {model_name} думает...",
        "empty_response": "Получен пустой ответ.",
        "error_unexpected": "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.",
        "error_rate_limit": "Слишком много запросов. Пожалуйста, подождите минуту.",
        "error_not_found": "Эта модель сейчас недоступна. Пожалуйста, выберите другую.",
        "error_auth": "Ошибка аутентификации. Проверьте API-ключ.",
    },
    'en': {
        "welcome_choose_lang": "Please select your language. / Пожалуйста, выберите ваш язык.",
        "welcome_after_lang": "Language set!\n\nI'm ready to work. The chat history has been cleared.\n\n"
                              "To begin, choose a role for the bot or skip this step.",
        "start_after_restart": "Hello, {user_name}!\n\nI'm ready to work. The chat history has been cleared.\n\n"
                               "To begin, choose a role for the bot or skip this step.",
        "role_chosen": "✅ Role successfully changed! Now just send me a message.",
        "role_skipped": "Alright, using the default assistant. Now just send me a message.",
        "role_reset": "✅ Role has been reset to default.",
        "role_set_custom": "✅ New role has been set!",
        "prompt_for_custom_role": "Please send me the new text for the system prompt. To reset to default, send `-`.",
        "btn_skip_role": "➡️ Skip",
        "btn_set_custom_role": "✏️ Set custom role",
        "btn_back_to_settings": "⬅️ Back to settings",
        "btn_memory_on": "✅ Memory ON",
        "btn_memory_off": "❌ Memory OFF",
        "btn_choose_role": "🎭 Choose Role",
        "btn_show_settings": "ℹ️ Show Settings",
        "btn_back_to_chat": "⬅️ Back to Chat",
        "options_menu_title": "⚙️ Chat Settings:",
        "roles_menu_title": "Select a pre-defined role or enter your own:",
        "model_menu_title": "Current model: `{current_model}`\n\nSelect a new one:",
        "model_changed": "✅ Model changed to `{model_name}`.",
        "current_settings_title": "Current Settings:\n\n"
                                  "🧠 *Model:* `{model}`\n"
                                  "💾 *Memory:* {memory}\n"
                                  "🎭 *Role:* \n`{prompt}`",
        "admin_no_permission": "⛔️ You do not have permission to execute this command.",
        "thinking_indicator": "🧠 {model_name} is thinking...",
        "empty_response": "Received an empty response.",
        "error_unexpected": "An unexpected error occurred. Please try again later.",
        "error_rate_limit": "Too many requests. Please wait a minute.",
        "error_not_found": "This model is currently unavailable. Please choose another one.",
        "error_auth": "Authentication error. Please check the API key.",
    }
}
