@echo off

REM crea el entorno virtual e instala dependencias automaticamente en Windows
REM Ejecutar desde: MC-crawler\ (raíz del proyecto)

cd /d %~dp0..
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
pause
