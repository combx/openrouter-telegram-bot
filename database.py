# -*- coding: utf-8 -*-
import sqlite3
import logging
from typing import List, Dict, Any, Optional

DB_FILE = "bot_data.db"
logger = logging.getLogger(__name__)

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS user_settings ( chat_id INTEGER PRIMARY KEY, first_name TEXT, username TEXT, language TEXT, model TEXT, memory_enabled BOOLEAN, system_prompt TEXT, is_banned BOOLEAN NOT NULL DEFAULT 0, state TEXT ) ''')
        table_info = cursor.execute("PRAGMA table_info(user_settings);").fetchall()
        column_names = [col['name'] for col in table_info]
        if 'is_banned' not in column_names: cursor.execute('ALTER TABLE user_settings ADD COLUMN is_banned BOOLEAN NOT NULL DEFAULT 0;')
        if 'first_name' not in column_names: cursor.execute('ALTER TABLE user_settings ADD COLUMN first_name TEXT;')
        if 'username' not in column_names: cursor.execute('ALTER TABLE user_settings ADD COLUMN username TEXT;')
        if 'state' not in column_names: cursor.execute('ALTER TABLE user_settings ADD COLUMN state TEXT;')
        if 'language' not in column_names: cursor.execute("ALTER TABLE user_settings ADD COLUMN language TEXT;"); logger.info("Column 'language' added.")
        cursor.execute(''' CREATE TABLE IF NOT EXISTS messages ( id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER NOT NULL, user_message_id INTEGER NOT NULL, user_message_text TEXT NOT NULL, bot_response_id INTEGER NOT NULL, bot_response_text TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ) ''')
        conn.commit()
    logger.info("Database initialized.")

def get_user_settings(chat_id: int, default_model: str, default_prompt: str) -> Dict[str, Any]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_settings WHERE chat_id = ?", (chat_id,))
        user_data = cursor.fetchone()
        if user_data: return dict(user_data)
        else: return { 'chat_id': chat_id, 'first_name': None, 'username': None, 'language': None, 'model': default_model, 'memory_enabled': True, 'system_prompt': default_prompt, 'is_banned': False, 'state': None }

def save_user_settings(chat_id: int, settings: Dict[str, Any]):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(''' INSERT OR REPLACE INTO user_settings (chat_id, first_name, username, language, model, memory_enabled, system_prompt, is_banned, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (chat_id, settings.get('first_name'), settings.get('username'), settings.get('language'), settings.get('model'), settings.get('memory_enabled'), settings.get('system_prompt'), settings.get('is_banned', False), settings.get('state')))
        conn.commit()

def set_user_state(chat_id: int, state: Optional[str]):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_settings SET state = ? WHERE chat_id = ?", (state, chat_id))
        conn.commit()

def set_ban_status(chat_id: int, status: bool):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_settings SET is_banned = ? WHERE chat_id = ?", (1 if status else 0, chat_id))
        conn.commit()
    logger.info(f"Ban status for user {chat_id} set to {status}.")

def get_user_history(chat_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT ?', (chat_id, limit))
        return [dict(row) for row in reversed(cursor.fetchall())]

def add_to_history(chat_id: int, pair: Dict[str, Any]):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO messages (chat_id, user_message_id, user_message_text, bot_response_id, bot_response_text) VALUES (?, ?, ?, ?, ?) ''', (chat_id, pair['user_message_id'], pair['user_message_text'], pair['bot_response_id'], pair['bot_response_text']))
        conn.commit()

def delete_last_history_pair(chat_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM messages WHERE chat_id = ?", (chat_id,))
        last_id_tuple = cursor.fetchone()
        if last_id_tuple and last_id_tuple[0] is not None:
            cursor.execute("DELETE FROM messages WHERE id = ?", (last_id_tuple[0],))
            conn.commit()
            logger.info(f"Deleted last history entry for chat {chat_id}")

def full_user_reset(chat_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_settings WHERE chat_id = ?", (chat_id,))
        cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        conn.commit()
    logger.info(f"Full reset for user {chat_id}.")

def get_bot_stats() -> Dict[str, int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_settings;")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM messages;")
        total_messages = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM messages WHERE DATE(timestamp, 'localtime') = DATE('now', 'localtime');")
        today_messages = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT chat_id) FROM messages WHERE DATE(timestamp, 'localtime') = DATE('now', 'localtime');")
        today_active_users = cursor.fetchone()[0]
        return {"total_users": total_users, "total_messages": total_messages, "today_messages": today_messages, "today_active_users": today_active_users}
        
def get_all_users_with_activity() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(''' SELECT u.chat_id, u.first_name, u.username, MAX(m.timestamp) as last_activity FROM user_settings u LEFT JOIN messages m ON u.chat_id = m.chat_id GROUP BY u.chat_id ORDER BY last_activity DESC ''')
        return [dict(row) for row in cursor.fetchall()]

def get_active_users_today() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(''' SELECT u.chat_id, u.first_name, u.username, MAX(m.timestamp) as last_activity FROM user_settings u JOIN messages m ON u.chat_id = m.chat_id WHERE DATE(m.timestamp, 'localtime') = DATE('now', 'localtime') GROUP BY u.chat_id ORDER BY last_activity DESC ''')
        return [dict(row) for row in cursor.fetchall()]
