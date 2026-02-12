from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from src.config import Config

class Keyboards:
    @staticmethod
    def main_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton("🤖 Model", callback_data="menu_model"),
                InlineKeyboardButton("🔑 My Key", callback_data="menu_key")
            ],
            [
                InlineKeyboardButton("👤 Profile", callback_data="menu_profile"),
                InlineKeyboardButton("🎭 Roles", callback_data="menu_roles")
            ]
        ]
        
        if is_admin:
            keyboard.append([
                InlineKeyboardButton("📊 Stats (Admin)", callback_data="admin_stats"),
                InlineKeyboardButton("🚫 Ban (Admin)", callback_data="admin_ban")
            ])
            
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def model_menu(current_model: str) -> InlineKeyboardMarkup:
        # TODO: Add dynamic list of top models
        keyboard = [
            [InlineKeyboardButton("🔎 Search Model", callback_data="model_search")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_main() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
