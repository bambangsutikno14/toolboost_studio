@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python "scripts/growth_audit.py"
pause
