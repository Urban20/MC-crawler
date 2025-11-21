@echo off

REM script que utilizo para compilar a .exe en Windows

REM paso 1: crear un entorno virtual (python -m venv env)
REM paso 2: instalar Nuitka (pip install nuitka)
REM paso 3 : ejecutar este script

call env\Scripts\activate

nuitka --standalone --lto=yes --jobs=5 --plugin-enable=pylint-warnings --output-filename=MC-crawler --include-data-files=escan.exe=escan.exe --include-data-file=db/servers.db=db/servers.db --include-data-file=db/crackeados.db=db/crackeados.db --include-data-file=configuracion/configuracion.ini=configuracion/configuracion.ini --include-package=rich --include-package=pygments main.py

pause