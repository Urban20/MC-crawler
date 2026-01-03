@echo off

REM crea el entorno virtual e instala dependencias automaticamente en Windows

python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
pause