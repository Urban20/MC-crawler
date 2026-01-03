'un script encargado de instalar el escaner para Windows de forma automatizada sin intervencion del usuario'
import platform
import os
from escaner.gopython import BINARIO
import requests
import time
from utilidades.conectividad import conectividad
import sys

ejecutable = f'{BINARIO}.exe' # similar al bin de gopython pero este explicita su extension
VERSION_BIN = 'V3.0' # version del escaner a instalar
ruta_bin = os.path.join(os.path.dirname(__file__),ejecutable)
url_exe = f'https://github.com/Urban20/MC-crawler/releases/download/{VERSION_BIN}/{ejecutable}'

def descargar_exe():
    'intenta descargar el escaner automaticamente'

    if not conectividad():
        sys.exit(1)
        

    delay = 3
    if platform.system() != 'Windows':
        return

    if os.path.exists(ruta_bin):
        print('\n✓ escaner encontrado\n')
        time.sleep(delay)
        return
   
    req = requests.get(url_exe)
    
    if req.status_code != 200:
        print(f'fuente no disponible, codigo de estado: {req.status_code}')
        time.sleep(delay)
        return
    

    if str(input(f'descargar {ejecutable} automaticamente s/n >> ')).strip().lower() != 's':

        return
    
    print(f'\ndescargando {ejecutable} ...\n')
    time.sleep(delay)
    
    with open(ruta_bin,'wb') as ej:
        ej.write(req.content)
    
    print('\n✓ descarga exitosa\n')
    time.sleep(delay)

    
    