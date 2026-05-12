#!/bin/bash

# Script que utilizo para compilar a ejecutable en Linux
# Ejecutar desde: MC-crawler/ (raíz del proyecto)

# Paso 1: crear un entorno virtual (ejecutar dependencias.sh)
# Paso 2: verificar que Nuitka esté instalado
# Paso 3: ejecutar este script

cd "$(dirname "$0")/.." || exit
source env/bin/activate

nuitka --standalone --lto=yes --low-memory --plugin-enable=pylint-warnings --output-filename=MC-crawler --include-data-files=escaner/binario/escan.exe=escaner/binario/escan.exe --include-data-file=db/servers.db=db/servers.db --include-data-file=db/crackeados.db=db/crackeados.db --include-data-file=configuracion/configuracion.ini=configuracion/configuracion.ini --include-package=rich --include-package=pygments main.py
