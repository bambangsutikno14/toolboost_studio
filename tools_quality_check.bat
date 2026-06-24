@echo off
cd /d "%~dp0"
set "PYTHONPATH=%CD%"
if exist ".venv\Scripts\activate.bat" call .venv\Scripts\activate.bat
python scripts\tools_quality_check.py
pause
