"""
JARVIS - Mouse va Klaviatura Boshqaruvi
PyAutoGUI orqali to'liq boshqaruv
"""

import pyautogui
import pyperclip
import time
import webbrowser


class MouseKeyboardControl:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.screen_width, self.screen_height = pyautogui.size()
    
    # ==================== MOUSE ====================
    
    def move_mouse(self, x, y, duration=0.5):
        pyautogui.moveTo(x, y, duration=duration)
        return f"✅ Mouse ({x}, {y}) ga siljitildi."
    
    def click(self, x=None, y=None, button='left', clicks=1):
        if x and y:
            pyautogui.click(x, y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)
        return f"✅ Click bajarildi."
    
    def double_click(self, x=None, y=None):
        if x and y:
            pyautogui.doubleClick(x, y)
        else:
            pyautogui.doubleClick()
        return "✅ Double click bajarildi."
    
    def right_click(self, x=None, y=None):
        if x and y:
            pyautogui.rightClick(x, y)
        else:
            pyautogui.rightClick()
        return "✅ Right click bajarildi."
    
    def scroll(self, amount, x=None, y=None):
        if x and y:
            pyautogui.scroll(amount, x, y)
        else:
            pyautogui.scroll(amount)
        return f"✅ Scroll bajarildi."
    
    def get_mouse_position(self):
        pos = pyautogui.position()
        return {"x": pos.x, "y": pos.y}
    
    # ==================== KLAVIATURA ====================
    
    def type_text(self, text, interval=0.02):
        if any(ord(c) > 127 for c in text):
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
        else:
            pyautogui.typewrite(text, interval=interval)
        return f"✅ Matn yozildi."
    
    def press_key(self, key):
        pyautogui.press(key)
        return f"✅ '{key}' bosildi."
    
    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        return f"✅ {'+'.join(keys)} bosildi."
    
    def press_enter(self):
        pyautogui.press('enter')
        return "✅ Enter bosildi."
    
    def copy(self):
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)
        return pyperclip.paste()
    
    def paste(self, text=None):
        if text:
            pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        return "✅ Paste bajarildi."
    
    def select_all(self):
        pyautogui.hotkey('ctrl', 'a')
        return "✅ Hammasi tanlandi."
    
    def switch_window(self):
        pyautogui.hotkey('alt', 'tab')
        return "✅ Oyna almashtirildi."
    
    # ==================== BRAUZER ====================
    
    def open_browser_url(self, url):
        webbrowser.open(url)
        return f"✅ Brauzerda ochildi: {url}"
    
    def search_google(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"✅ Google da qidirilmoqda: {query}"
    
    def search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return f"✅ YouTube da qidirilmoqda: {query}"
