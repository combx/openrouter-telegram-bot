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
                InlineKeyboardButton("🎭 Roles", callback_data="menu_roles"),
                InlineKeyboardButton("🗑 Clear Context", callback_data="clear_context")
            ]
        ]
        
        if is_admin:
            keyboard.append([
                InlineKeyboardButton("📊 Stats (Admin)", callback_data="admin_stats"),
                InlineKeyboardButton("🚫 Ban (Admin)", callback_data="admin_ban"),
                InlineKeyboardButton("📜 Logs (Admin)", callback_data="admin_logs")
            ])
            
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def model_menu(current_model: str, models_list: list[dict] = None, page: int = 0) -> InlineKeyboardMarkup:
        keyboard = []
        PAGE_SIZE = 5
        
        # Add dynamic buttons for top free models
        if models_list:
            start_index = page * PAGE_SIZE
            end_index = start_index + PAGE_SIZE
            current_page_models = models_list[start_index:end_index]
            
            for model in current_page_models:
                name = model.get('name', 'Unknown')
                # Shorten name if too long
                if len(name) > 30:
                    name = name[:27] + "..."
                
                model_id = model.get('id')
                # Mark current model
                if model_id == current_model:
                    name = f"✅ {name}"
                
                keyboard.append([InlineKeyboardButton(name, callback_data=f"set_model_{model_id}")])
            
            # Pagination Controls
            if end_index < len(models_list):
                 keyboard.append([InlineKeyboardButton(f"⬇️ Show More ({len(models_list) - end_index} left)", callback_data=f"menu_model_page_{page + 1}")])
        
        keyboard.append([InlineKeyboardButton("🔎 Manual Search", callback_data="model_search")])
        keyboard.append([
            InlineKeyboardButton("🗑 Clear Context", callback_data="clear_context"),
            InlineKeyboardButton("⬅️ Back", callback_data="menu_main")
        ])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_main() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
