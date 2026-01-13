from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import rich
from colorama import init
from rich.table import Table
from rich.live import Live
import time
from configuracion import configuracion
import subprocess
import os
import sys
import shutil


init()
consola = Console()

NEGRITA = '\033[1m'
VERSION = 'V6.3' # version del programa
VIOLETA = '\033[0;95m'
RESET = '\033[0m '
AMARILLO = '\033[0;33m'
CELESTE = '\033[0;96m'
ROJO = '\033[0;31m'
VERDE = '\033[0;32m'

LOGO = f'''
\033[1;35m██▄  ▄██  ▄▄▄▄     ▄█████ ▄▄▄▄   ▄▄▄  ▄▄   ▄▄ ▄▄    ▄▄▄▄▄ ▄▄▄▄  
\033[0;35m██ ▀▀ ██ ██▀▀▀ ▄▄▄ ██     ██▄█▄ ██▀██ ██ ▄ ██ ██    ██▄▄  ██▄█▄ 
\033[2;35m██    ██ ▀████     ▀█████ ██ ██ ██▀██  ▀█▀█▀  ██▄▄▄ ██▄▄▄ ██ ██ \n{RESET}{VERSION}\n
escrito por: Urb@n 
                                                                                                                                                                                      
'''

def imprimir_logo():
    x,_ = shutil.get_terminal_size()
    for linea in LOGO.splitlines():
        sys.stdout.write(linea.center(x)+'\n')
        sys.stdout.flush()

def ver_config():
    config = f'''

    - REDES:

        hilos: {configuracion.HILOS}
        tiempo de espera entre server: {configuracion.TIMEOUT} seg

    - BOT:

        timeout del bot : {configuracion.TIMEOUT_BOT} seg
    
    - ARCHIVOS:

        archivo de guardado .txt: {configuracion.FILTRADOS}
    
    - PURGADO:

        timeout de purgado: {configuracion.TIMEOUT_PURGADO}
        reintentos: {configuracion.REINTENTOS}    

    - DISEÑO:

        tema: {configuracion.COLOR}
    '''

    rich.print(Panel(config,title='configuracion'))

    

def crear_tabla(estados : list):
    tabla = Table(expand=True,)
    tabla.add_column('servicio',justify='center')
    tabla.add_column('estado',justify='center')

    with Live(tabla):
        for servicio,estado in zip(['Oracle','Amazonaws','Google','Hetzner'],estados):
            tabla.add_row(servicio,estado)
            time.sleep(0.5)


def limpiar(logo = True):


    for com in ('cls','clear'):
        if subprocess.run(com,shell=True,stderr=open(os.devnull,'w')).returncode == 0:
            break     
        
    if logo:
        imprimir_logo()        


def info_server(cuerpo : str,titulo : str =''):
    consola = Console()
    msg = f'''\n
# {titulo}

{cuerpo}

'''
    md = Markdown(msg)
    consola.print(md)



def pagina(n_pagina : int):
    etiqueta = f'# Pagina {n_pagina}'
    consola.print(Markdown(etiqueta,style='white'),style=configuracion.COLOR)