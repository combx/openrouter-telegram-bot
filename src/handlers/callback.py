from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from src.utils.keyboard import Keyboards
from src.services.user_service import update_user_model, set_custom_key, get_user, update_user_role, set_user_state
from src.database import get_db
from src.services.openrouter import OpenRouterService
from src.config import Config

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    async for session in get_db():
        user = await get_user(session, user_id)
        if not user: return

        if data == "menu_main":
            is_admin = (user_id == Config.ADMIN_ID)
            await query.edit_message_text(
                "Main Menu:",
                reply_markup=Keyboards.main_menu(is_admin)
            )
            
        elif data == "menu_model":
            # Fetch top free models
            service = OpenRouterService(api_key=Config.OPENROUTER_API_KEY)
            models = await service.get_free_models()
            
            await query.edit_message_text(
                f"Current Model: `{user.current_model}`\n\nSelect a top free model or search manually:",
                reply_markup=Keyboards.model_menu(user.current_model, models),
                parse_mode="Markdown"
            )
        
        elif data.startswith("set_model_"):
            model_id = data.replace("set_model_", "")
            await update_user_model(session, user_id, model_id)
            await query.edit_message_text(
                f"✅ Model set to `{model_id}`",
                reply_markup=Keyboards.back_to_main(),
                parse_mode="Markdown"
            )

        elif data == "menu_profile":
            stats = f"""
👤 **Profile**
ID: `{user.id}`
Name: {user.full_name}
Model: `{user.current_model}`
Role: `{user.current_role}`
Usage: {user.usage_count} requests
Key Type: {"Custom" if user.custom_api_key else "Shared"}
"""
            await query.edit_message_text(
                stats,
                reply_markup=Keyboards.back_to_main(),
                parse_mode="Markdown"
            )

        elif data == "model_search":
            await set_user_state(session, user_id, "SEARCH_MODE")
            await query.edit_message_text(
                "To search for a model, just type: `search <query>`\nExample: `search gpt-4`",
                reply_markup=Keyboards.back_to_main(),
                parse_mode="Markdown"
            )

        elif data == "menu_key":
            key_status = "Custom 🔑" if user.custom_api_key else "Shared 🌐"
            text = f"Current Key: {key_status}\n\nUsing a custom key allows you to use paid models and bypass limits."
            keyboard = [
                [InlineKeyboardButton("✏️ Set Custom Key", callback_data="set_key_input")],
                [InlineKeyboardButton("🗑 Reset Key", callback_data="reset_key")],
                [InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]
            ]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            
        elif data == "set_key_input":
            await set_user_state(session, user_id, "SET_CUSTOM_KEY")
            await query.edit_message_text(
                "Please send your OpenRouter API Key.\nIt will be stored securely.",
                reply_markup=Keyboards.back_to_main()
            )

        elif data == "reset_key":
            await set_custom_key(session, user_id, None)
            await query.edit_message_text("✅ Custom key removed.", reply_markup=Keyboards.back_to_main())

        elif data == "menu_roles":
            roles = {
                "assistant": "Helpful Assistant",
                "translator": "Translator",
                "coder": "Python Developer",
                "copywriter": "Copywriter"
            }
            keyboard = [[InlineKeyboardButton(name, callback_data=f"set_role_{code}")] for code, name in roles.items()]
            keyboard.append([InlineKeyboardButton("✏️ Custom Role", callback_data="set_role_custom")])
            keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
            
            await query.edit_message_text("Choose a role:", reply_markup=InlineKeyboardMarkup(keyboard))
            
        elif data.startswith("set_role_"):
            role_code = data.split("set_role_")[1]
            if role_code == "custom":
                # TODO: Implement custom role input similar to custom key
                await query.edit_message_text("Feature not implemented yet.", reply_markup=Keyboards.back_to_main())
            else:
                await update_user_role(session, user_id, role_code)
                await query.edit_message_text(f"✅ Role set to `{role_code}`", reply_markup=Keyboards.main_menu((user_id == Config.ADMIN_ID)))

        elif data == "clear_context":
            from src.services.user_service import clear_user_context
            await clear_user_context(session, user_id)
            await query.answer("Memory cleared! 🧠✨", show_alert=True)
            # await query.edit_message_text("Context cleared.", reply_markup=Keyboards.main_menu((user_id == Config.ADMIN_ID)))
