"""
JARVIS - Internet Moduli
Ob-havo, valyuta, yangiliklar, qidiruv
"""

import requests
from datetime import datetime
from config import OPENWEATHER_API_KEY, WEATHER_CITY


class InternetModule:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Jarvis-Assistant/1.0'})
    
    def get_weather(self, city=None):
        city = city or WEATHER_CITY
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "lang": "uz"}
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            if response.status_code == 200:
                return {
                    "city": city, "temp": round(data["main"]["temp"]),
                    "feels_like": round(data["main"]["feels_like"]),
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
            return {"error": data.get("message", "Xato")}
        except Exception as e:
            return {"error": f"Ob-havo olib bo'lmadi: {e}"}


    def get_weather_text(self, city=None):
        weather = self.get_weather(city)
        if "error" in weather:
            return f"❌ {weather['error']}"
        return (
            f"🌤 {weather['city']} ob-havosi:\n"
            f"🌡 Harorat: {weather['temp']}°C (his qilinadi: {weather['feels_like']}°C)\n"
            f"☁️ Holat: {weather['description']}\n"
            f"💧 Namlik: {weather['humidity']}%\n"
            f"💨 Shamol: {weather['wind_speed']} m/s"
        )
    
    def get_exchange_rates(self, base="USD"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            return {
                "USD_UZS": data["rates"].get("UZS", "N/A"),
                "RUB_UZS": round(data["rates"].get("UZS", 0) / data["rates"].get("RUB", 1), 2),
                "date": data.get("date", "")
            }
        except Exception as e:
            return {"error": f"Valyuta kursini olib bo'lmadi: {e}"}
    
    def get_currency_text(self):
        rates = self.get_exchange_rates()
        if "error" in rates:
            return f"❌ {rates['error']}"
        return (
            f"💰 Valyuta kurslari:\n"
            f"🇺🇸 1 USD = {rates['USD_UZS']:,.0f} UZS\n"
            f"🇷🇺 1 RUB = {rates['RUB_UZS']:,.0f} UZS\n"
            f"📅 Sana: {rates['date']}"
        )
    
    def get_news_text(self):
        return "📰 Yangiliklar moduli ulangan (API kalit kerak)."
    
    def get_time_text(self):
        now = datetime.now()
        days_uz = {
            "Monday": "Dushanba", "Tuesday": "Seshanba",
            "Wednesday": "Chorshanba", "Thursday": "Payshanba",
            "Friday": "Juma", "Saturday": "Shanba", "Sunday": "Yakshanba"
        }
        day_uz = days_uz.get(now.strftime("%A"), now.strftime("%A"))
        return f"🕐 Hozir soat {now.strftime('%H:%M:%S')}, {day_uz}, {now.strftime('%d.%m.%Y')}"
    
    def search_web(self, query):
        try:
            url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_redirect": 1}
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            results = []
            if data.get("Abstract"):
                results.append({"title": data.get("Heading", ""), "text": data["Abstract"]})
            for topic in data.get("RelatedTopics", [])[:5]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({"title": topic.get("Text", "")[:100], "text": topic.get("Text", "")})
            return results
        except Exception as e:
            return [{"title": "Xato", "text": f"Qidirib bo'lmadi: {e}"}]
