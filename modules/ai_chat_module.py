"""
JARVIS - AI Chat Moduli
Google Gemini API orqali aqlli suhbat
"""

from config import GEMINI_API_KEY, ASSISTANT_NAME, OWNER_NAME, MAX_CONVERSATION_HISTORY

# Himoyalangan import
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("[!] google-generativeai kutubxonasi topilmadi!")
    print("[!] O'rnatish: pip install google-generativeai")
    print("[!] Demo rejimda ishlayman.\n")


class AIChat:
    def __init__(self):
        self.conversation_history = []
        self.model = None
        self.chat = None
        
        if GENAI_AVAILABLE and GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=self._get_system_prompt()
                )
                self.chat = self.model.start_chat(history=[])
                print("  ✓ AI (Gemini) ulandi")
            except Exception as e:
                print(f"  ✗ AI ulanmadi: {e}")
        else:
            print("  ⚠ AI demo rejimda (kutubxona yoki API kalit yo'q)")
    
    def _get_system_prompt(self):
        return f"""Sen {ASSISTANT_NAME} — {OWNER_NAME}ning shaxsiy AI yordamchisisan.

XULQ-ATVOR QOIDALARI:
1. Har doim o'zbek tilida gapir (agar boshqa til so'ralmasa)
2. Qisqa, aniq va foydali javoblar ber
3. Iron Man filimidagi JARVIS kabi muloyim, aqlli va professional bo'l
4. {OWNER_NAME}ga "xo'jayin" yoki ismini ishlatib murojaat qil
5. Hazil-mutoyiba ham qo'shib tur, lekin o'rinli paytda
6. Agar bilmasang, ochiq ayt va qidirish taklif qil
7. Proaktiv bo'l — maslahat va takliflar ber
8. Xavfsizlik haqida doim ogohlantir (shubhali buyruqlarda)

QOBILIYATLARING:
- Har qanday savolga javob berish
- Matn yozish (referat, xat, kod, post, rezyume)
- Kompyuterni boshqarish
- Internet dan ma'lumot olish
- Reja tuzish va eslatmalar
- Kod yozish va tushuntirish
- Tarjima qilish
- Kreativ g'oyalar berish

JAVOB FORMATI:
- Javoblar qisqa bo'lsin (1-3 gap), agar batafsil so'ralmasa
- Texnik javoblarda kod bloklar ishlatilsin
- Ro'yxatlar uchun raqamli yoki nuqtali ro'yxat
"""
    
    def ask(self, question):
        # Agar AI ulanmagan bo'lsa — demo javob
        if not self.chat:
            return self._demo_response(question)
        
        try:
            response = self.chat.send_message(question)
            answer = response.text
            
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            if len(self.conversation_history) > MAX_CONVERSATION_HISTORY * 2:
                self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY * 2:]
            
            return answer
        except Exception as e:
            return f"Kechirasiz, xatolik yuz berdi: {str(e)}"
    
    def _demo_response(self, text):
        """API kalit yoki kutubxona bo'lmaganda demo javoblar"""
        text_lower = text.lower()
        if any(w in text_lower for w in ["salom", "hey", "hi"]):
            return f"Salom, {OWNER_NAME}! Men {ASSISTANT_NAME}. Hozir demo rejimda ishlayman. To'liq AI uchun: pip install google-generativeai"
        elif any(w in text_lower for w in ["kim", "nima"]):
            return f"Men {ASSISTANT_NAME} — sizning AI yordamchingizman. Demo rejim. To'liq ishlashim uchun google-generativeai o'rnating va .env ga API kalit kiriting."
        else:
            return (f"🤖 Demo rejim: To'liq AI javoblar uchun:\n"
                    f"1. CMD da: pip install google-generativeai\n"
                    f"2. .env faylga: GEMINI_API_KEY=sizning_kalitingiz\n"
                    f"3. API kalit: https://makersuite.google.com/app/apikey")
    
    def ask_with_context(self, question, context=""):
        full_prompt = f"Kontekst: {context}\n\nSavol: {question}"
        return self.ask(full_prompt)
    
    def analyze_image(self, image_path, question="Bu rasmda nima bor?"):
        if not GENAI_AVAILABLE:
            return "❌ Rasm tahlili uchun google-generativeai kerak."
        try:
            import PIL.Image
            img = PIL.Image.open(image_path)
            vision_model = genai.GenerativeModel("gemini-1.5-flash")
            response = vision_model.generate_content([question, img])
            return response.text
        except Exception as e:
            return f"Rasmni tahlil qilishda xato: {e}"
    
    def generate_code(self, description, language="python"):
        prompt = f"Quyidagi vazifa uchun {language} tilida kod yoz:\n{description}\n\nFaqat kodni ber, kommentariyali bo'lsin."
        return self.ask(prompt)
    
    def translate(self, text, target_lang="uzbek"):
        prompt = f"Quyidagi matnni {target_lang} tiliga tarjima qil:\n\n{text}"
        return self.ask(prompt)
    
    def summarize(self, text):
        prompt = f"Quyidagi matnning qisqacha xulosasini ber (3-5 gap):\n\n{text}"
        return self.ask(prompt)
    
    def write_text(self, text_type, details):
        prompt = f"Quyidagi turdagi matn yoz: {text_type}\nTafsilotlar: {details}\n\nProfessional va sifatli matn yoz."
        return self.ask(prompt)
    
    def reset_conversation(self):
        self.chat = self.model.start_chat(history=[])
        self.conversation_history = []
