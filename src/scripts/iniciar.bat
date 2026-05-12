@echo off

REM Ejecutar desde: MC-crawler\ (raíz del proyecto)

cd /d %~dp0..
call env\Scripts\activate

python main.py
