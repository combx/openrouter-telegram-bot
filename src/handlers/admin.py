from telegram import Update
from telegram.ext import ContextTypes
from src.config import Config
from src.database import get_db
from sqlalchemy import select, func, desc, update
from src.database.models import User, ErrorLog
import io

async def admin_check(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await admin_check(user_id): return
    
    async for session in get_db():
        # Count total users
        result_users = await session.execute(select(func.count(User.id)))
        total_users = result_users.scalar()
        
        # Sum total requests
        result_req = await session.execute(select(func.sum(User.usage_count)))
        total_requests = result_req.scalar() or 0
        
        # Get top 5 users by usage
        result_top = await session.execute(select(User).order_by(desc(User.usage_count)).limit(5))
        top_users = result_top.scalars().all()
        
        top_text = "\n".join([f"{u.id} ({u.full_name}): {u.usage_count}" for u in top_users])
        
        await update.message.reply_text(
            f"📊 **Statistics**\n\n"
            f"Total Users: {total_users}\n"
            f"Total Requests: {total_requests}\n\n"
            f"🏆 **Top Active Users:**\n{top_text}",
            parse_mode="Markdown"
        )

async def admin_ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Usage: /ban <user_id>
    user_id = update.effective_user.id
    if not await admin_check(user_id): return
    
    try:
        user_to_ban = int(context.args[0])
        async for session in get_db():
            stmt = update(User).where(User.id == user_to_ban).values(is_banned=True)
            await session.execute(stmt)
            await session.commit()
            await update.message.reply_text(f"✅ User {user_to_ban} has been banned.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /ban <user_id>")

async def admin_unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Usage: /unban <user_id>
    user_id = update.effective_user.id
    if not await admin_check(user_id): return
    
    try:
        user_to_unban = int(context.args[0])
        async for session in get_db():
            stmt = update(User).where(User.id == user_to_unban).values(is_banned=False)
            await session.execute(stmt)
            await session.commit()
            await update.message.reply_text(f"✅ User {user_to_unban} has been unbanned.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /unban <user_id>")

async def admin_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await admin_check(user_id): return
    
    async for session in get_db():
        result = await session.execute(select(ErrorLog).order_by(desc(ErrorLog.timestamp)).limit(20))
        logs = result.scalars().all()
        
        if not logs:
            await update.message.reply_text("✅ No errors logged in the last 20 entries.")
            return
            
        # Format logs
        log_lines = []
        for l in logs:
            log_lines.append(f"[{l.timestamp.strftime('%Y-%m-%d %H:%M')}] User {l.user_id}: {l.error_text[:100]}")
            
        log_text = "\n".join(log_lines)
        
        if len(log_text) > 4000:
            # Send as file if too big
            file = io.BytesIO(log_text.encode())
            file.name = "error_logs.txt"
            await update.message.reply_document(file, caption="⚠️ Recent Errors")
        else:
            await update.message.reply_text(f"⚠️ **Recent Errors:**\n\n```\n{log_text}\n```", parse_mode="Markdown")
