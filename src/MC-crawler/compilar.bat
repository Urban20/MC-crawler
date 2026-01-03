@echo off

REM script que utilizo para compilar a .exe en Windows

REM paso 1: crear un entorno virtual (ejecutar dependencias.bat)
REM paso 2: verificar que Nuitka este instalado
REM paso 3 : ejecutar este script

call env\Scripts\activate

nuitka --standalone --lto=yes --jobs=5 --plugin-enable=pylint-warnings --output-filename=MC-crawler --include-data-files=escaner/binario/escan.exe=escaner/binario/escan.exe --include-data-file=db/servers.db=db/servers.db --include-data-file=db/crackeados.db=db/crackeados.db --include-data-file=configuracion/configuracion.ini=configuracion/configuracion.ini --include-package=rich --include-package=pygments main.py

pause