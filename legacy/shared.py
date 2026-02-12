# -*- coding: utf-8 -*-
import os
from functools import wraps
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import database as db
from translations import TRANSLATIONS

# --- SHARED CONSTANTS ---
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
AVAILABLE_MODELS = { "Meta Llama 3.3 8B": "meta-llama/llama-3.3-8b-instruct:free", "OpenAI GPT-OSS 20B": "openai/gpt-oss-20b:free", "Nvidia Nemotron 9B": "nvidia/nemotron-nano-9b-v2:free", "Qwen3 235B": "qwen/qwen3-235b-a22b:free", "DeepSeek Chimera R1T2": "tngtech/deepseek-r1t2-chimera:free", "GLM 4.5 Air": "z-ai/glm-4.5-air:free" }
MODEL_ID_TO_NAME = {v: k for k, v in AVAILABLE_MODELS.items()}
DEFAULT_MODEL = "tngtech/deepseek-r1t2-chimera:free"
AVAILABLE_ROLES = {
    'ru': { "assistant": "Ты — полезный ИИ-ассистент.", "python_expert": "Ты — ведущий Python-разработчик...", "translator": "Ты — профессиональный переводчик...", "marketer": "Ты — опытный маркетолог...", "storyteller": "Ты — талантливый рассказчик...", "poet": "Ты — поэт...", "chef": "Ты — шеф-повар..." },
    'en': { "assistant": "You are a helpful AI assistant.", "python_expert": "You are a senior Python developer...", "translator": "You are a professional translator...", "marketer": "You are an experienced marketer...", "storyteller": "You are a talented storyteller...", "poet": "You are a poet...", "chef": "You are a chef..." }
}
SMART_ASSISTANT_ROLE = {
    'ru': "Ты — умный ассистент, созданный для помощи в решении сложных задач. Отвечай развернуто, структурированно и дружелюбно. Используй Markdown для форматирования, где это уместно.",
    'en': "You are a smart assistant, designed to help with complex tasks. Respond in a detailed, structured, and friendly manner. Use Markdown for formatting where appropriate."
}

# --- SHARED HELPER FUNCTIONS ---
def get_user_lang(chat_id: int) -> str:
    with db.get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM user_settings WHERE chat_id = ?", (chat_id,))
        user_data = cursor.fetchone()
        if user_data and user_data['language']: return user_data['language']
    return 'ru'

def _(chat_id: int, key: str, **kwargs) -> str:
    lang = get_user_lang(chat_id)
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, f"_{key}_").format(**kwargs)

def admin_only(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            no_perm_text = _(user_id, "admin_no_permission")
            if update.message: await update.message.reply_text(no_perm_text)
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

# --- SHARED KEYBOARD FUNCTIONS ---
def create_model_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(name, callback_data=f"model_{model_id}")] for name, model_id in AVAILABLE_MODELS.items()])

def create_options_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    settings = db.get_user_settings(chat_id, DEFAULT_MODEL, "")
    memory_text = _(chat_id, 'btn_memory_on') if settings.get('memory_enabled', True) else _(chat_id, 'btn_memory_off')
    return InlineKeyboardMarkup([ [InlineKeyboardButton(memory_text, callback_data="toggle_memory")], [InlineKeyboardButton(_(chat_id, 'btn_choose_role'), callback_data="show_roles_menu")], [InlineKeyboardButton(_(chat_id, 'btn_show_settings'), callback_data="show_status")], [InlineKeyboardButton(_(chat_id, 'btn_back_to_chat'), callback_data="close_options")] ])

def create_roles_selection_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    lang = get_user_lang(chat_id)
    keyboard = [[InlineKeyboardButton(prompt.split('.')[0], callback_data=f"role_{key}")] for key, prompt in AVAILABLE_ROLES[lang].items()]
    keyboard.extend([ [InlineKeyboardButton(_(chat_id, 'btn_skip_role'), callback_data="role_skip")], [InlineKeyboardButton(_(chat_id, 'btn_set_custom_role'), callback_data="set_custom_prompt")], [InlineKeyboardButton(_(chat_id, 'btn_back_to_settings'), callback_data="back_to_options")] ])
    return InlineKeyboardMarkup(keyboard)

def create_language_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[ InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"), InlineKeyboardButton("English 🇬🇧", callback_data="lang_en") ]])
