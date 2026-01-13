'un script encargado de instalar el escaner para Windows de forma automatizada sin intervencion del usuario'
import platform
import os
from escaner.gopython import BINARIO
import requests
import time
from utilidades.conectividad import conectividad
import sys

ejecutable = f'{BINARIO}.exe' # similar al bin de gopython pero este explicita su extension
VERSION_BIN = 'V3.1' # version del escaner a instalar
ruta_bin = os.path.join(os.path.dirname(__file__),ejecutable) # similar a la ruta de gopython.py con la diferencia de que este involucra su extension .exe
url_exe = f'https://github.com/Urban20/MC-crawler/releases/download/{VERSION_BIN}/{ejecutable}'

def descargar_exe():
    'intenta descargar el escaner automaticamente'

    if not conectividad():
        sys.exit(1)
        

    delay = 1
    if platform.system() != 'Windows':
        return

    if os.path.exists(ruta_bin):
        print('\n✓ escaner encontrado\n')
        time.sleep(delay)
        return
   
    req = requests.get(url_exe)
    print('escaner no encontrado, descargando ...')
    if req.status_code != 200:
        print(f'fuente no disponible, codigo de estado: {req.status_code}')
        time.sleep(delay)
        sys.exit(1)
    

    if str(input(f'descargar {ejecutable} {VERSION_BIN} automaticamente s/n >> ')).strip().lower() != 's':

        return
    
    print(f'\ndescargando {ejecutable} ...\n')
    print(f'fuente: {url_exe}')
    time.sleep(delay)
    
    with open(ruta_bin,'wb') as ej:
        ej.write(req.content)
    
    print('\n✓ descarga exitosa\n')
    time.sleep(delay)

    
    