from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import rich
import sys
from colorama import init
from rich.table import Table
from rich.live import Live
import time
import configuracion


init()
consola = Console()

NEGRITA = '\033[1m'
VERSION = 'V6.0' # version del programa
VIOLETA = '\033[0;95m'
RESET = '\033[0m '
FONDO_V = '\033[0;105m'
AMARILLO = '\033[0;33m'
CELESTE = '\033[0;96m'
ROJO = '\033[0;31m'
VERDE = '\033[0;32m'

LOGO = f'''   *           '     *
                   *                *   '              *          *
           '              _______----_______                                 *   
                    °'==(______( o_(_____( ;)                    '
                                /|\\                *           
                               / | \\    {VIOLETA}MC-Crawler {VERSION}{RESET}                  
                              /  |  \\   buscador de servers de Minecraft java           
                             /   |   \\      *                                 
                            /    |    \\   {FONDO_V}Escrito por Urb@n{RESET}
                        
                    github : https://github.com/Urban20
'''
ADVERTENCIA = f'{AMARILLO}\n[!] advertencia: El antivirus puede bloquear el correcto funcionamiento del programa y/o dar falsos positivos\n{RESET}'

def ver_config():
    config = f'''

    - REDES:

     hilos: {configuracion.HILOS}
     tiempo de espera entre server: {configuracion.TIMEOUT} seg

    - ARCHIVOS:

     archivo de guardado .txt: {configuracion.FILTRADOS}

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
    sys.stdout.write('\033c')
    sys.stdout.flush()
    if logo:
        print(LOGO)
        print(ADVERTENCIA)


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