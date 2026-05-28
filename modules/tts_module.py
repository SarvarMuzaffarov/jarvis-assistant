"""
JARVIS - Text-to-Speech Moduli
Edge TTS yordamida tabiiy erkak ovozida gapirish
"""

import edge_tts
import asyncio
import pygame
import os
import tempfile
import threading
from config import TTS_VOICE, TTS_RATE, TTS_VOLUME


class TextToSpeech:
    def __init__(self):
        pygame.mixer.init()
        self.is_speaking = False
        self.temp_dir = tempfile.mkdtemp()
        self.voice = TTS_VOICE
        self.rate = TTS_RATE
        self.volume = TTS_VOLUME
        
        self.available_voices = {
            "uzbek_male": "uz-UZ-SardorNeural",
            "uzbek_female": "uz-UZ-MadinaNeural",
            "russian_male": "ru-RU-DmitryNeural",
            "russian_female": "ru-RU-SvetlanaNeural",
            "english_male": "en-US-GuyNeural",
            "english_female": "en-US-JennyNeural",
        }
    
    def speak(self, text):
        if not text:
            return
        self.is_speaking = True
        thread = threading.Thread(target=self._speak_async, args=(text,), daemon=True)
        thread.start()
    
    def speak_sync(self, text):
        if not text:
            return
        self.is_speaking = True
        self._speak_async(text)
    
    def _speak_async(self, text):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._generate_and_play(text))
            loop.close()
        except Exception as e:
            print(f"[TTS xatosi]: {e}")
            self._fallback_speak(text)
        finally:
            self.is_speaking = False
    
    async def _generate_and_play(self, text):
        temp_file = os.path.join(self.temp_dir, "jarvis_speech.mp3")
        
        communicate = edge_tts.Communicate(
            text=text, voice=self.voice, rate=self.rate, volume=self.volume
        )
        await communicate.save(temp_file)
        
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        try:
            pygame.mixer.music.unload()
            os.remove(temp_file)
        except:
            pass
    
    def _fallback_speak(self, text):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            voices = engine.getProperty('voices')
            for voice in voices:
                if "male" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[Fallback TTS xatosi]: {e}")
    
    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.is_speaking = False
    
    def set_voice(self, voice_key):
        if voice_key in self.available_voices:
            self.voice = self.available_voices[voice_key]
    
    def cleanup(self):
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass
