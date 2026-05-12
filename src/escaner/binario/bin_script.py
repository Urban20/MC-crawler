'un script encargado de instalar el escaner para Windows de forma automatizada sin intervencion del usuario'
import platform
import os
from escaner.gopython import BINARIO,ruta
import requests
import time
from utilidades.conectividad import conectividad
import sys

ejecutable = f'{BINARIO}.exe' # similar al bin de gopython pero este explicita su extension
VERSION_BIN = 'V3.1' # version del escaner a instalar
ruta_bin = os.path.join(os.path.dirname(__file__),ejecutable) # similar a la ruta de gopython.py con la diferencia de que este involucra su extension .exe
url_exe = f'https://github.com/Urban20/MC-crawler/releases/download/{VERSION_BIN}/{ejecutable}'
doc_compilar = 'leer.txt'

documentacion = '''
[LEER]


Si estas leyendo esto es porque falta el escaner de servidores el cual no se incluye en Linux por cuestiones de compatibilidad:
Este binario es sumamente necesario y se debe compilar manualmente

La carpeta binario/ es la carpeta donde se debe introducir dicho archivo solicitado
Este binario es el responsable de los escaneos de puertos masivos para el descubrimiento de servidores.

Pasos para la compilacion:

1) instalar Golang
2) ingresar a la carpeta escaner/golang
3) ejecutar el siguiente comando : go build .
4) arrastrar el binario generado a escaner/binario

'''

def check_binario_linux():

    if platform.system() != 'Linux':
        return
    
    if not os.path.exists(ruta):
        
        print(documentacion)
        input('enter para salir')

        sys.exit(1)
    

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

    
    