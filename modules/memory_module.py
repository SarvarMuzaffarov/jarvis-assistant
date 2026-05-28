"""
JARVIS - Xotira Moduli
Shaxsiy ma'lumotlarni eslab qolish (SQLite)
"""

import sqlite3
import os
from datetime import datetime
from config import MEMORY_DB, DATA_DIR


class MemoryModule:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.db_path = MEMORY_DB
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS personal_info (
            key TEXT PRIMARY KEY, value TEXT, category TEXT, updated_at TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, timestamp TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT,
            due_date TEXT, is_done INTEGER DEFAULT 0, created_at TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY, value TEXT, context TEXT, created_at TEXT,
            access_count INTEGER DEFAULT 0)""")
        conn.commit()
        conn.close()


    def save_personal(self, key, value, category="general"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO personal_info VALUES (?,?,?,?)",
                      (key, value, category, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return f"✅ Eslab qoldim: {key} = {value}"
    
    def get_personal(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM personal_info WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_all_personal(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value, category FROM personal_info")
        results = cursor.fetchall()
        conn.close()
        return {row[0]: {"value": row[1], "category": row[2]} for row in results}
    
    def remember(self, key, value, context=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO memory VALUES (?,?,?,?,0)",
                      (key, value, context, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return f"✅ Eslab qoldim: {key}"
    
    def recall(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value, context FROM memory WHERE key LIKE ?", (f"%{key}%",))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_reminder(self, title, description="", due_date=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reminders (title,description,due_date,created_at) VALUES (?,?,?,?)",
                      (title, description, due_date, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return f"✅ Eslatma qo'shildi: {title}"
    
    def get_reminders(self, include_done=False):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if include_done:
            cursor.execute("SELECT id, title, description, due_date, is_done FROM reminders ORDER BY due_date")
        else:
            cursor.execute("SELECT id, title, description, due_date, is_done FROM reminders WHERE is_done=0 ORDER BY due_date")
        results = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "title": r[1], "description": r[2], "due_date": r[3], "is_done": bool(r[4])} for r in results]
    
    def complete_reminder(self, reminder_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET is_done=1 WHERE id=?", (reminder_id,))
        conn.commit()
        conn.close()
        return "✅ Vazifa bajarildi!"
    
    def save_conversation(self, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (role,content,timestamp) VALUES (?,?,?)",
                      (role, content, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_context_summary(self):
        personal = self.get_all_personal()
        reminders = self.get_reminders()
        summary = "FOYDALANUVCHI PROFILI:\n"
        for key, data in personal.items():
            summary += f"- {key}: {data['value']}\n"
        if reminders:
            summary += "\nFAOL VAZIFALAR:\n"
            for r in reminders[:5]:
                summary += f"- {r['title']}\n"
        return summary
