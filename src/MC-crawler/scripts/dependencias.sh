#!/bin/bash

# Crea el entorno virtual e instala dependencias automáticamente en Linux
# Ejecutar desde: MC-crawler/ (raíz del proyecto)

cd "$(dirname "$0")/.." || exit
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
