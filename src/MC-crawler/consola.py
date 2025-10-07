from rich.console import Console
from rich.markdown import Markdown
import sys
from colorama import init


init()
VERSION = 'V3.1' # version del programa
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
    etiqueta = f'# {FONDO_V}Pagina {n_pagina}{RESET}'
    consola = Console()
    md = Markdown(etiqueta)
    consola.print(md)