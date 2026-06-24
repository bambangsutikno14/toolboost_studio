@echo off
cd /d "%~dp0"
echo Starting ADSENSE_SAAS_AUTO...
if not exist ".venv\Scripts\activate.bat" (
  echo Virtual environment belum ada. Jalankan ads_full_power.py dulu.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
set PYTHONPATH=%CD%\app
python -m waitress --host=127.0.0.1 --port=8000 app.app:app
pause
