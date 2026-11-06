@echo off
echo ========================================================
echo Iniciando Servidor FastAPI con conexion a Supabase
echo ========================================================
cd /d "%~dp0"
call venv\Scripts\activate
uvicorn main:app --reload --port 8000
pause
