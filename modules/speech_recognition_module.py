"""
JARVIS - Ovozni Aniqlash Moduli
Wake word + Doimiy tinglash + O'zbek tilida nutqni matnga aylantirish
"""

import speech_recognition as sr
import threading
import time
from config import WAKE_WORDS, SPEECH_LANGUAGE


class SpeechRecognizer:
    def __init__(self, callback=None, wake_word_callback=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.is_active = False
        self.callback = callback
        self.wake_word_callback = wake_word_callback
        self.listen_thread = None
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0
    
    def start_listening(self):
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        print("[Tinglash boshlandi...]")
    
    def stop_listening(self):
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
    
    def _listen_loop(self):
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                text = self._recognize(audio)
                
                if text:
                    text_lower = text.lower().strip()
                    
                    if not self.is_active:
                        if self._check_wake_word(text_lower):
                            self.is_active = True
                            if self.wake_word_callback:
                                self.wake_word_callback()
                            command = self._extract_command(text_lower)
                            if command and self.callback:
                                self.callback(command)
                    else:
                        if text_lower in ["to'xta", "yetarli", "rahmat", "bas"]:
                            self.is_active = False
                        elif self.callback:
                            self.callback(text)
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"[Speech xatosi]: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"[Xato]: {e}")
                time.sleep(1)
    
    def _recognize(self, audio):
        try:
            return self.recognizer.recognize_google(audio, language=SPEECH_LANGUAGE)
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            try:
                return self.recognizer.recognize_google(audio, language="ru-RU")
            except:
                return None
    
    def _check_wake_word(self, text):
        for wake_word in WAKE_WORDS:
            if wake_word in text:
                return True
        return False
    
    def _extract_command(self, text):
        for wake_word in WAKE_WORDS:
            if wake_word in text:
                parts = text.split(wake_word, 1)
                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip()
        return None
    
    def listen_once(self):
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                return self._recognize(audio)
        except Exception as e:
            return None
