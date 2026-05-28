"""
╔══════════════════════════════════════════════════════════════╗
║          ⚡ J.A.R.V.I.S - AI YORDAMCHI v1.0 ⚡              ║
║     Just A Rather Very Intelligent System                    ║
║     O'zbek tilidagi shaxsiy AI yordamchi                    ║
╚══════════════════════════════════════════════════════════════╝

Ishga tushirish: python main.py
"""

import sys
import os
import threading
import time

from config import ASSISTANT_NAME, OWNER_NAME
from modules.command_processor import CommandProcessor
from modules.ai_chat_module import AIChat
from modules.tts_module import TextToSpeech
from modules.memory_module import MemoryModule
from modules.internet_module import InternetModule
from modules.gui_module import JarvisGUI


class Jarvis:
    def __init__(self):
        print(f"⚡ {ASSISTANT_NAME} yuklanmoqda...")
        self.command_processor = CommandProcessor()
        self.ai_chat = AIChat()
        self.tts = TextToSpeech()
        self.memory = MemoryModule()
        self.internet = InternetModule()
        self.gui = None
        self.speech = None
        self.system_control = None
        self.mouse_keyboard = None
        self.telegram = None
        self.gmail = None
        self._load_system_modules()
        self.gui = JarvisGUI(
            on_text_input=self.handle_input,
            on_mic_toggle=self.toggle_microphone,
            on_close=self.shutdown
        )
        print(f"✅ {ASSISTANT_NAME} tayyor!")


    def _load_system_modules(self):
        try:
            from modules.system_control_module import SystemControl
            self.system_control = SystemControl()
            print("  ✓ Tizim boshqaruvi yuklandi")
        except Exception as e:
            print(f"  ✗ Tizim boshqaruvi: {e}")
        try:
            from modules.mouse_keyboard_module import MouseKeyboardControl
            self.mouse_keyboard = MouseKeyboardControl()
            print("  ✓ Mouse/Klaviatura yuklandi")
        except Exception as e:
            print(f"  ✗ Mouse/Klaviatura: {e}")
        try:
            from modules.speech_recognition_module import SpeechRecognizer
            self.speech = SpeechRecognizer(
                callback=self._on_speech_recognized,
                wake_word_callback=self._on_wake_word
            )
            print("  ✓ Ovoz tanish yuklandi")
        except Exception as e:
            print(f"  ✗ Ovoz tanish: {e}")
        try:
            from modules.telegram_module import TelegramModule
            self.telegram = TelegramModule(message_callback=self._on_telegram_message)
            print("  ✓ Telegram yuklandi")
        except Exception as e:
            print(f"  ✗ Telegram: {e}")
        try:
            from modules.gmail_module import GmailModule
            self.gmail = GmailModule()
            print("  ✓ Gmail yuklandi")
        except Exception as e:
            print(f"  ✗ Gmail: {e}")
    
    def run(self):
        self.tts.speak(f"Salom {OWNER_NAME}! Men {ASSISTANT_NAME}, xizmatdaman.")
        self.gui.start()
    
    def handle_input(self, text):
        if not text.strip():
            return
        cmd_type, params = self.command_processor.process(text)
        if self.gui:
            self.gui.show_thinking()
        response = self._execute_command(cmd_type, params, text)
        if response and self.gui:
            self.gui.add_message("jarvis", response)
            self.gui.hide_thinking()
        if response and len(response) < 300:
            self.tts.speak(self._clean_for_speech(response))
        self.memory.save_conversation("user", text)
        self.memory.save_conversation("assistant", response or "")


    def _execute_command(self, cmd_type, params, original_text):
        try:
            if cmd_type == "open_app" and self.system_control:
                return self.system_control.open_app(params or original_text)
            elif cmd_type == "close_app" and self.system_control:
                return self.system_control.close_app(params or original_text)
            elif cmd_type == "screenshot" and self.system_control:
                path = self.system_control.take_screenshot()
                return f"✅ Skrinshot saqlandi: {path}"
            elif cmd_type == "volume" and self.system_control:
                import re
                nums = re.findall(r'\d+', str(params))
                level = int(nums[0]) if nums else 50
                return self.system_control.set_volume(level)
            elif cmd_type == "brightness" and self.system_control:
                import re
                nums = re.findall(r'\d+', str(params))
                level = int(nums[0]) if nums else 50
                return self.system_control.set_brightness(level)
            elif cmd_type == "mute" and self.system_control:
                return self.system_control.mute_volume()
            elif cmd_type == "unmute" and self.system_control:
                return self.system_control.unmute_volume()
            elif cmd_type == "wifi_on" and self.system_control:
                return self.system_control.toggle_wifi(True)
            elif cmd_type == "wifi_off" and self.system_control:
                return self.system_control.toggle_wifi(False)
            elif cmd_type == "lock" and self.system_control:
                return self.system_control.lock_computer()
            elif cmd_type == "shutdown" and self.system_control:
                return self.system_control.shutdown_computer()
            elif cmd_type == "restart" and self.system_control:
                return self.system_control.restart_computer()
            elif cmd_type == "system_info" and self.system_control:
                info = self.system_control.get_system_info()
                return (f"💻 Tizim holati:\n⚡ CPU: {info['cpu_percent']}%\n"
                        f"🧠 RAM: {info['ram_used_percent']}%\n"
                        f"💾 Disk: {info['disk_used_percent']}%\n"
                        f"⏱ Uptime: {info['uptime_hours']} soat")
            elif cmd_type == "weather":
                return self.internet.get_weather_text()
            elif cmd_type == "currency":
                return self.internet.get_currency_text()
            elif cmd_type == "news":
                return self.internet.get_news_text()
            elif cmd_type == "time":
                return self.internet.get_time_text()
            elif cmd_type == "google_search" and self.mouse_keyboard:
                self.mouse_keyboard.search_google(params or original_text)
                return f"🔍 Google da qidirilmoqda: {params}"
            elif cmd_type == "youtube_search" and self.mouse_keyboard:
                self.mouse_keyboard.search_youtube(params or original_text)
                return f"▶️ YouTube da qidirilmoqda: {params}"
            elif cmd_type == "remember":
                if params and ":" in str(params):
                    key, value = str(params).split(":", 1)
                    return self.memory.remember(key.strip(), value.strip())
                return self.memory.remember(str(params), str(params))
            elif cmd_type == "reminder":
                return self.memory.add_reminder(str(params))
            elif cmd_type == "telegram_send" and self.telegram:
                return self.telegram.send_message(str(params))
            elif cmd_type == "clear_chat" and self.gui:
                self.gui.clear_chat()
                return None
            elif cmd_type == "help":
                return self.command_processor.get_help_text()
            elif cmd_type == "ai_chat":
                context = self.memory.get_context_summary()
                return self.ai_chat.ask_with_context(original_text, context)
            else:
                return self.ai_chat.ask(original_text)
        except Exception as e:
            return f"❌ Xatolik: {str(e)}"


    def toggle_microphone(self, enable):
        if not self.speech:
            if self.gui:
                self.gui.add_message("system", "❌ Mikrofon moduli yuklanmagan.")
            return
        if enable:
            self.speech.start_listening()
        else:
            self.speech.stop_listening()
    
    def _on_speech_recognized(self, text):
        if self.gui:
            self.gui.add_message("user", f"🎤 {text}")
        self.handle_input(text)
    
    def _on_wake_word(self):
        self.tts.speak("Ha, xo'jayin, tinglayapman!")
    
    def _on_telegram_message(self, msg_data):
        if self.gui:
            self.gui.add_message("system", f"📱 Telegram | {msg_data['sender']}: {msg_data['text']}")
    
    def _clean_for_speech(self, text):
        import re
        text = re.sub(r'[✅❌⚡🎤🖥💻🧠💾🔋⏱📂🌤🌡☁️💧💨💰📰📱📧🔍▶️📋●─═╔╗║╚╝]', '', text)
        return re.sub(r'\s+', ' ', text).strip()
    
    def shutdown(self):
        print(f"\n⚡ {ASSISTANT_NAME} o'chmoqda...")
        self.tts.speak("Xayr, xo'jayin!")
        time.sleep(1)
        if self.speech:
            self.speech.stop_listening()
        self.tts.cleanup()


if __name__ == "__main__":
    try:
        jarvis = Jarvis()
        jarvis.run()
    except KeyboardInterrupt:
        print("\n⚡ Jarvis to'xtatildi.")
    except Exception as e:
        print(f"❌ Kritik xato: {e}")
        import traceback
        traceback.print_exc()
