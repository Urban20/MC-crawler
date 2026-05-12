#!/bin/bash

# Ejecutar desde: MC-crawler/ (raíz del proyecto)

cd "$(dirname "$0")/.." || exit
source env/bin/activate
python main.py
