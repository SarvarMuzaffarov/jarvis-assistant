"""
JARVIS - Telegram Integratsiyasi
Xabar o'qish, yozish, yuborish
"""

import asyncio
import threading
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramModule:
    def __init__(self, message_callback=None):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.message_callback = message_callback
        self.bot = Bot(token=self.bot_token)
        self.app = None
        self.is_running = False
        self.received_messages = []
    
    def start_bot(self):
        thread = threading.Thread(target=self._run_bot, daemon=True)
        thread.start()
        self.is_running = True
    
    def _run_bot(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.app = Application.builder().token(self.bot_token).build()
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
            loop.run_until_complete(self.app.initialize())
            loop.run_until_complete(self.app.start())
            loop.run_until_complete(self.app.updater.start_polling())
            loop.run_forever()
        except Exception as e:
            print(f"[Telegram xatosi]: {e}")


    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        msg_data = {
            "sender": message.from_user.first_name,
            "text": message.text,
            "chat_id": message.chat_id,
            "date": str(message.date)
        }
        self.received_messages.append(msg_data)
        if self.message_callback:
            self.message_callback(msg_data)
    
    def send_message(self, text, chat_id=None):
        chat_id = chat_id or self.chat_id
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.send_message(chat_id=chat_id, text=text))
            loop.close()
            return "✅ Telegram xabar yuborildi."
        except Exception as e:
            return f"❌ Xabar yuborib bo'lmadi: {e}"
    
    def get_recent_messages(self, count=10):
        return self.received_messages[-count:]
    
    def stop_bot(self):
        self.is_running = False
