@echo off
setlocal
if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
)
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
if "%ADMIN_PASSWORD%"=="" set ADMIN_PASSWORD=flyxadmin
set FLASK_ENV=production
echo Starting FlyX locally on http://127.0.0.1:5000
python app.py
