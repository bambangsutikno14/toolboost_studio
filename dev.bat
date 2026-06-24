@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
set PYTHONPATH=%CD%\app
python app\app.py
pause
