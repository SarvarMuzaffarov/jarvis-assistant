"""
JARVIS - Konfiguratsiya fayli
Barcha sozlamalar shu yerda saqlanadi
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== ASOSIY SOZLAMALAR ====================
ASSISTANT_NAME = "Jarvis"
OWNER_NAME = "Sarvar"  # O'zingizning ismingiz
WAKE_WORDS = ["jarvis", "yordamchi", "salom jarvis", "hey jarvis"]

# ==================== API KALITLARI ====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_API_KEY_HERE")

# ==================== OVOZ SOZLAMALARI ====================
TTS_VOICE = "uz-UZ-SardorNeural"  # O'zbek erkak ovozi (Edge TTS)
TTS_RATE = "+0%"
TTS_VOLUME = "+0%"
SPEECH_LANGUAGE = "uz-UZ"

# ==================== TIZIM SOZLAMALARI ====================
SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Jarvis_Screenshots")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
MEMORY_DB = os.path.join(DATA_DIR, "memory.db")

# ==================== GUI SOZLAMALARI ====================
THEME = "iron_man"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ALWAYS_ON_TOP = True
OPACITY = 0.95

# ==================== INTERNET ====================
WEATHER_CITY = "Tashkent"
CURRENCY_BASE = "USD"

# ==================== XOTIRA ====================
MAX_CONVERSATION_HISTORY = 50

# ==================== DASTURLAR YO'LLARI (Windows) ====================
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "telegram": r"C:\Users\{user}\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "notepad": r"C:\Windows\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "explorer": r"C:\Windows\explorer.exe",
}
