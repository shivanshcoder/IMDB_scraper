@echo off
:loop
start python init.py
timeout /t 800>null
taskkill /f /im python.exe >nul
timeout /t 7 >null
goto loop