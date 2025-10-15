from rich.console import Console
from rich.markdown import Markdown
import sys
from colorama import init
from rich.table import Table
from rich.live import Live
import time


init()
VERSION = 'V4.1' # version del programa
VIOLETA = '\033[0;95m'
RESET = '\033[0m '
FONDO_V = '\033[0;105m'
AMARILLO = '\033[0;33m'

LOGO = f'''   *           '     *
                   *                *   '              *          *
           '              _______----_______                                 *   
                    °'==(______( o_(_____( ;)                    '
                                /|\\                *           
                               / | \\    {VIOLETA}MC-Crawler {VERSION}{RESET}                  
                              /  |  \\   buscador de servers de Minecraft java           
                             /   |   \\      *                                 
                            /    |    \\   {FONDO_V}Escrito por => Urb@n{RESET}
                        
                    github : https://github.com/Urban20
'''
ADVERTENCIA = f'{AMARILLO}\n[!] advertencia: El antivirus puede bloquear el correcto funcionamiento del programa y/o dar falsos positivos\n{RESET}'

def crear_tabla(estados : list):
    tabla = Table(expand=True,)
    tabla.add_column('servicio',justify='center')
    tabla.add_column('estado',justify='center')

    with Live(tabla):
        for servicio,estado in zip(['oracle','amazonaws','google'],estados):
            tabla.add_row(servicio,estado)
            time.sleep(0.5)


def limpiar():
    sys.stdout.write('\033c')
    sys.stdout.flush()
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
    consola = Console()
    consola.print(Markdown(etiqueta,style='white'),style='medium_purple3')