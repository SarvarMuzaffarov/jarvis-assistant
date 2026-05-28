"""
⚡ J.A.R.V.I.S - Web Versiya
Flask + WebSocket orqali brauzerda ishlash
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import google.generativeai as genai
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="web_templates", static_folder="web_static")
app.config['SECRET_KEY'] = 'jarvis-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# ==================== AI SOZLASH ====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OWNER_NAME = "Sarvar"
ASSISTANT_NAME = "Jarvis"

ai_chat = None
conversation_history = []
memory_store = {}


def init_ai():
    """AI modelini ishga tushirish"""
    global ai_chat
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return False
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=f"""Sen {ASSISTANT_NAME} — {OWNER_NAME}ning shaxsiy AI yordamchisisan.

QOIDALAR:
1. Har doim o'zbek tilida gapir (agar boshqa til so'ralmasa)
2. Qisqa, aniq va foydali javoblar ber
3. Iron Man filimidagi JARVIS kabi muloyim, aqlli va professional bo'l
4. {OWNER_NAME}ga "xo'jayin" yoki ismini ishlatib murojaat qil
5. Hazil ham qo'shib tur
6. Proaktiv bo'l — maslahat va takliflar ber

QOBILIYATLARING:
- Har qanday savolga javob berish (ilm, texnologiya, biznes, kundalik)
- Matn yozish (referat, xat, kod, post, rezyume)
- Kod yozish va tushuntirish
- Tarjima qilish
- Reja tuzish va maslahat berish
- Kreativ g'oyalar berish
- Matematika va hisob-kitob

JAVOB FORMATI:
- Javoblar qisqa bo'lsin (1-5 gap), agar batafsil so'ralmasa
- Kod uchun markdown format ishlatilsin
- Ro'yxatlar uchun raqamli yoki nuqtali ro'yxat
"""
        )
        ai_chat = model.start_chat(history=[])
        return True
    except Exception as e:
        print(f"AI xatosi: {e}")
        return False


# ==================== WEB ROUTES ====================

@app.route('/')
def index():
    """Asosiy sahifa"""
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Tizim holati"""
    return jsonify({
        "status": "online",
        "ai_ready": ai_chat is not None,
        "assistant_name": ASSISTANT_NAME,
        "owner_name": OWNER_NAME,
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%d.%m.%Y")
    })


# ==================== WEBSOCKET EVENTS ====================

@socketio.on('connect')
def handle_connect():
    """Client ulanganda"""
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Xayrli tong"
    elif hour < 18:
        greeting = "Xayrli kun"
    else:
        greeting = "Xayrli kech"
    
    emit('message', {
        'role': 'jarvis',
        'text': f"⚡ {greeting}, {OWNER_NAME}! Men {ASSISTANT_NAME} — xizmatdaman.\n\nMenga har qanday savol bering yoki buyruq yozing!",
        'time': datetime.now().strftime("%H:%M")
    })


@socketio.on('user_message')
def handle_message(data):
    """Foydalanuvchi xabarini qayta ishlash"""
    text = data.get('text', '').strip()
    if not text:
        return
    
    # Buyruqni tekshirish
    response = process_command(text)
    
    emit('message', {
        'role': 'jarvis',
        'text': response,
        'time': datetime.now().strftime("%H:%M")
    })


def process_command(text):
    """Buyruqlarni qayta ishlash"""
    text_lower = text.lower().strip()
    
    # === VAQT ===
    if any(w in text_lower for w in ["soat", "vaqt", "time", "sana"]):
        now = datetime.now()
        days = {"Monday": "Dushanba", "Tuesday": "Seshanba", "Wednesday": "Chorshanba",
                "Thursday": "Payshanba", "Friday": "Juma", "Saturday": "Shanba", "Sunday": "Yakshanba"}
        day = days.get(now.strftime("%A"), now.strftime("%A"))
        return f"🕐 Hozir soat {now.strftime('%H:%M:%S')}, {day}, {now.strftime('%d.%m.%Y')}"
    
    # === YORDAM ===
    if any(w in text_lower for w in ["yordam", "help", "buyruqlar", "nima qila olasan"]):
        return get_help_text()
    
    # === ESLAB QOLISH ===
    if any(w in text_lower for w in ["eslab qol", "yodla", "remember"]):
        parts = text.split(":", 1) if ":" in text else text.split(" ", 2)
        if len(parts) > 1:
            key = parts[-2].strip() if len(parts) > 2 else "ma'lumot"
            value = parts[-1].strip()
            memory_store[key] = value
            return f"✅ Eslab qoldim: {value}"
        return "❌ Nima eslab qolishim kerak? Masalan: 'eslab qol: mening yoshim 25'"
    
    # === ESLASH ===
    if any(w in text_lower for w in ["eslat", "nima eslab qolding", "xotira"]):
        if memory_store:
            text = "🧠 Men eslab qolganlarim:\n\n"
            for k, v in memory_store.items():
                text += f"• {k}: {v}\n"
            return text
        return "🧠 Hozircha hech narsa eslab qolmaganman."
    
    # === TOZALASH ===
    if any(w in text_lower for w in ["tozala", "clear"]):
        return "__CLEAR__"
    
    # === AI CHAT ===
    if ai_chat:
        try:
            response = ai_chat.send_message(text)
            return response.text
        except Exception as e:
            return f"❌ AI xatosi: {str(e)}"
    else:
        return demo_response(text)


def demo_response(text):
    """API kalit bo'lmaganda demo javoblar"""
    text_lower = text.lower()
    
    if any(w in text_lower for w in ["salom", "hey", "hi"]):
        return f"Salom, {OWNER_NAME}! Qanday yordam bera olaman? 😊"
    elif any(w in text_lower for w in ["kim", "nima", "qanday"]):
        return (f"Men {ASSISTANT_NAME} — sizning shaxsiy AI yordamchingizman! "
                f"Hozir demo rejimda ishlayman. To'liq ishlashim uchun Gemini API kalitini kiriting.")
    elif any(w in text_lower for w in ["ob-havo", "havo"]):
        return "🌤 Demo rejim: Ob-havo ma'lumotlari uchun API kalit kerak.\nGemini API kalitini .env faylga kiriting."
    elif any(w in text_lower for w in ["kod", "code", "dastur"]):
        return ("💻 Men kod yozishda yordam bera olaman! Masalan:\n"
                "• Python, JavaScript, C++ va boshqa tillar\n"
                "• Xatolarni tuzatish\n"
                "• Algoritm tushuntirish\n\n"
                "⚠️ To'liq ishlashim uchun Gemini API kerak.")
    else:
        return (f"🤖 Demo rejim: Men hozir to'liq ishlay olmayman.\n\n"
                f"To'liq AI javoblar uchun:\n"
                f"1. https://makersuite.google.com/app/apikey dan API kalit oling\n"
                f"2. .env faylga GEMINI_API_KEY=your_key qo'shing\n"
                f"3. Dasturni qayta ishga tushiring\n\n"
                f"Lekin 'yordam' deb yozsangiz, buyruqlar ro'yxatini ko'rasiz!")


def get_help_text():
    return """⚡ **JARVIS BUYRUQLARI:**

🧠 **AQLLI SUHBAT:**
• Har qanday savol bering — AI javob beradi
• Kod yozishni so'rang
• Tarjima, referat, xat yozish
• Maslahat va g'oyalar

📝 **XOTIRA:**
• `eslab qol: [ma'lumot]` — Saqlash
• `xotira` — Eslab qolganlarni ko'rish

⏰ **VAQT:**
• `soat` yoki `vaqt` — Hozirgi vaqt

⚙️ **BOSHQA:**
• `tozala` — Chatni tozalash
• `yordam` — Shu ro'yxat

💡 **Maslahat:** Har qanday savolni o'zbek tilida bering!"""


# ==================== ISHGA TUSHIRISH ====================

if __name__ == '__main__':
    print("⚡ JARVIS Web versiya yuklanmoqda...")
    
    if init_ai():
        print("✅ AI tayyor (Gemini ulangan)")
    else:
        print("⚠️ AI demo rejimda (API kalit yo'q)")
    
    print(f"🌐 Brauzerda oching: http://localhost:5000")
    print(f"   Yoki: http://127.0.0.1:5000")
    print()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
