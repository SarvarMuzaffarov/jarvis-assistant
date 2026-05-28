"""
JARVIS - Buyruqlarni Qayta Ishlash Moduli
"""

import re


class CommandProcessor:
    def __init__(self):
        self.commands = {
            "open_app": {"keywords": ["och", "ishga tushir", "open", "run"]},
            "close_app": {"keywords": ["yop", "o'chir", "close", "kill"]},
            "screenshot": {"keywords": ["skrinshot", "screenshot", "ekranni ol"]},
            "volume": {"keywords": ["ovoz", "volume", "tovush"]},
            "brightness": {"keywords": ["yorqinlik", "brightness"]},
            "weather": {"keywords": ["ob-havo", "havo", "weather", "harorat"]},
            "currency": {"keywords": ["valyuta", "kurs", "dollar", "rubl"]},
            "news": {"keywords": ["yangilik", "news", "xabar"]},
            "time": {"keywords": ["soat", "vaqt", "time", "sana"]},
            "reminder": {"keywords": ["eslatma", "eslat", "reminder", "vazifa"]},
            "remember": {"keywords": ["eslab qol", "yodla", "remember"]},
            "telegram_send": {"keywords": ["telegramga yoz", "telegram yubor"]},
            "email_send": {"keywords": ["email yubor", "xat yubor", "pochta"]},
            "google_search": {"keywords": ["googleda qidir", "internetda qidir"]},
            "youtube_search": {"keywords": ["youtubeda qidir", "video qidir"]},
            "system_info": {"keywords": ["tizim holati", "system", "batareya", "ram"]},
            "lock": {"keywords": ["blokla", "qulf", "lock"]},
            "shutdown": {"keywords": ["kompyuterni o'chir", "shutdown"]},
            "restart": {"keywords": ["qayta yukla", "restart"]},
            "wifi_on": {"keywords": ["wifi yoq", "wi-fi yoq"]},
            "wifi_off": {"keywords": ["wifi o'chir", "wi-fi o'chir"]},
            "mute": {"keywords": ["ovozni o'chir", "mute"]},
            "unmute": {"keywords": ["ovozni yoq", "unmute"]},
            "clear_chat": {"keywords": ["tozala", "clear"]},
            "help": {"keywords": ["yordam", "help", "buyruqlar"]},
        }


    def process(self, text):
        text_lower = text.lower().strip()
        for cmd_type, cmd_data in self.commands.items():
            for keyword in cmd_data["keywords"]:
                if keyword in text_lower:
                    params = self._extract_params(text_lower, keyword)
                    return (cmd_type, params or text)
        return ("ai_chat", text)
    
    def _extract_params(self, text, keyword):
        # Keyword dan oldin yoki keyin turgan matnni olish
        parts = text.split(keyword)
        before = parts[0].strip() if parts[0].strip() else None
        after = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
        return after or before
    
    def get_help_text(self):
        return """⚡ JARVIS BUYRUQLARI:

🖥 TIZIM:
• "[dastur] och" — Dasturni ochish
• "[dastur] yop" — Dasturni yopish
• "skrinshot ol" — Ekran surati
• "ovoz 50" — Ovoz balandligi (0-100)
• "yorqinlik 70" — Ekran yorqinligi
• "wifi yoq/o'chir" — Wi-Fi boshqaruvi
• "blokla" — Ekran qulflash
• "tizim holati" — CPU, RAM, batareya

🌐 INTERNET:
• "ob-havo" — Bugungi ob-havo
• "valyuta kursi" — Dollar, rubl kursi
• "yangiliklar" — So'nggi yangiliklar
• "googleda qidir [...]" — Internet qidiruv
• "youtubeda qidir [...]" — Video qidiruv

📱 INTEGRATSIYA:
• "telegramga yoz [...]" — Xabar yuborish
• "email yubor [...]" — Pochta yuborish

🧠 AQLLI:
• Har qanday savol — AI javob beradi
• "eslab qol: [...]" — Ma'lumot saqlash
• "eslatma: [...]" — Eslatma qo'shish

⚙️ BOSHQA:
• "tozala" — Chat tozalash
• "yordam" — Shu ro'yxat
"""
