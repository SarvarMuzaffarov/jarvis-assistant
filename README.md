# ⚡ J.A.R.V.I.S - O'zbek Tilidagi AI Yordamchi

> Just A Rather Very Intelligent System — Shaxsiy AI yordamchi

## 📋 Xususiyatlar

- 🎤 **Ovozli suhbat** — Wake word ("Jarvis") + O'zbek tilida nutq tanish
- 🔊 **Tabiiy ovoz** — Edge TTS, erkak ovozida javob beradi
- 🧠 **AI Chat** — Google Gemini orqali aqlli suhbat
- 🖥 **Tizim boshqaruvi** — Dastur ochish/yopish, fayl qidirish, screenshot
- 🖱 **Mouse/Klaviatura** — To'liq boshqaruv
- 🌐 **Internet** — Ob-havo, valyuta, yangiliklar, qidiruv
- 📱 **Telegram** — Xabar yuborish/qabul qilish
- 📧 **Gmail** — Email yuborish
- 🧩 **Xotira** — Ma'lumotlarni eslab qolish (SQLite)
- ⚡ **GUI** — Iron Man uslubidagi chiroyli interfeys

## 🚀 O'rnatish

### Talablar
- Windows 10/11
- Python 3.10+
- Internet (API lar uchun)
- Mikrofon (ovozli suhbat uchun)

### Qadamlar

```bash
# 1. Yuklab olish
git clone https://github.com/SarvarMuzaffarov/jarvis-assistant.git
cd jarvis-assistant

# 2. O'rnatish (avtomatik)
install.bat

# 3. API kalitlarni sozlash (.env faylda)
# 4. Ishga tushirish
start.bat
```

### API kalitlarni olish
- 🤖 **Gemini**: https://makersuite.google.com/app/apikey
- 📱 **Telegram**: @BotFather orqali
- 🌤 **OpenWeather**: https://openweathermap.org/api

## 📖 Buyruqlar

| Buyruq | Tavsif |
|--------|--------|
| `chrome och` | Brauzer ochish |
| `skrinshot ol` | Ekran surati |
| `ovoz 50` | Ovoz 50% |
| `ob-havo` | Ob-havo |
| `valyuta kursi` | Kurslar |
| `eslab qol: ...` | Saqlash |
| `telegramga yoz: ...` | Xabar |
| `yordam` | Barcha buyruqlar |

## 📁 Struktura

```
jarvis-assistant/
├── main.py              # Asosiy dastur
├── config.py            # Sozlamalar
├── requirements.txt     # Kutubxonalar
├── .env.example         # API kalitlar namunasi
├── install.bat          # O'rnatish
├── start.bat            # Ishga tushirish
├── build_exe.bat        # EXE yaratish
└── modules/
    ├── ai_chat_module.py
    ├── speech_recognition_module.py
    ├── tts_module.py
    ├── system_control_module.py
    ├── mouse_keyboard_module.py
    ├── internet_module.py
    ├── telegram_module.py
    ├── gmail_module.py
    ├── memory_module.py
    ├── gui_module.py
    └── command_processor.py
```

## ⚙️ Sozlash

`config.py` faylida o'zgartiring:
- `OWNER_NAME` — Ismingiz
- `WAKE_WORDS` — Wake word lar
- `WEATHER_CITY` — Shahar

---

**Yaratuvchi: Sarvar Muzaffarov | 2024**
