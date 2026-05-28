@echo off
title JARVIS - O'rnatish
color 0A
echo ==============================
echo   JARVIS - O'RNATISH DASTURI
echo ==============================
echo.
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Python topilmadi! Python 3.10+ o'rnating: https://python.org
    pause
    exit /b
)
echo [*] Virtual environment yaratilmoqda...
python -m venv jarvis_env
call jarvis_env\Scripts\activate
echo [*] Kutubxonalar o'rnatilmoqda...
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env (
    copy .env.example .env
    echo [*] .env fayli yaratildi - API kalitlaringizni kiriting!
)
if not exist data mkdir data
echo.
echo ==============================
echo   O'RNATISH MUVAFFAQIYATLI!
echo   Ishga tushirish: start.bat
echo ==============================
pause
