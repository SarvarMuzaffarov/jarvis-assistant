@echo off
title JARVIS - EXE yaratish
color 0E
echo [*] EXE yaratilmoqda...
if exist jarvis_env\Scripts\activate (
    call jarvis_env\Scripts\activate
)
pyinstaller --noconfirm --onedir --windowed --name "Jarvis" --add-data "config.py;." --add-data "modules;modules" --add-data "data;data" --hidden-import "customtkinter" --hidden-import "edge_tts" --hidden-import "google.generativeai" --hidden-import "speech_recognition" --hidden-import "pyautogui" --hidden-import "psutil" --hidden-import "pygame" main.py
echo [OK] EXE yaratildi: dist\Jarvis\Jarvis.exe
pause
