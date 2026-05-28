@echo off
title J.A.R.V.I.S
color 0B
echo ⚡ JARVIS ishga tushmoqda...
if exist jarvis_env\Scripts\activate (
    call jarvis_env\Scripts\activate
)
python main.py
pause
