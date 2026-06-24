@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
  echo Virtual environment belum ada. Jalankan ads_full_power.py dulu.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
python "scripts/auto_content.py"
pause
