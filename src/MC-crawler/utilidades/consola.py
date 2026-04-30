from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.live import Live
import time
from configuracion import configuracion
import subprocess
import os
import sys
import shutil


consola = Console()
margen = ' ' * 2

NEGRITA = '\033[1m'
VERSION = 'V7.0' # version del programa
VIOLETA = '\033[0;95m'
RESET = '\033[0m '
AMARILLO = '\033[0;33m'
CELESTE = '\033[0;96m'
ROJO = '\033[0;31m'
VERDE = '\033[0;32m'
cmd = 'cls' if os.name == 'nt' else 'clear'

LOGO = f'''
\033[1;35m{' '*10}██▄  ▄██  ▄▄▄▄     ▄█████ ▄▄▄▄   ▄▄▄  ▄▄   ▄▄ ▄▄    ▄▄▄▄▄ ▄▄▄▄  
\033[0;35m{' '*10}██ ▀▀ ██ ██▀▀▀ ▄▄▄ ██     ██▄█▄ ██▀██ ██ ▄ ██ ██    ██▄▄  ██▄█▄ 
\033[2;35m{' '*10}██    ██ ▀████     ▀█████ ██ ██ ██▀██  ▀█▀█▀  ██▄▄▄ ██▄▄▄ ██ ██ \n
{RESET}{VERSION}\n
escrito por: Urb@n 
                                                                                                                                                                                      
'''
# etiquetas que se muestran en la consola como veredicto de los servidores
ET_CRACK = f'{VERDE}crackeado/no premium{RESET}'
ET_PREM = f'{ROJO}premium{RESET}'
ET_IND = 'indeterminado'
ET_TIM = f'{AMARILLO}tiempo agotado{RESET}'
ET_INC = f'{CELESTE}protocolo incompatible{RESET}'
ET_BAN = f'{VIOLETA}BANEADO{RESET}'
ET_MOD = f'{ROJO}MODEADO{RESET}'


def print2(texto : str,delay = 0.01,salto : bool = True):
    for c in texto:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    if salto:
        sys.stdout.write('\n')
        sys.stdout.flush()


def input2(texto : str,delay : float = 0.01):

    print2(texto,
           salto=False,
           delay=delay)
    
    salida = sys.stdin.readline()
    sys.stdin.flush()

    return str(salida)

def imprimir_logo():
    delay = 0.05
    x,_ = shutil.get_terminal_size()
    for linea in LOGO.splitlines():
        sys.stdout.write(linea.center(x)+'\n')
        sys.stdout.flush()
        time.sleep(delay)

def ver_config():
    limpiar()
    t='\n'
    
    seccion = configuracion.config
    print(VIOLETA + '\n' + margen + '[ configuraciones ]'.upper() + RESET + '\n\n')
    for k in seccion.sections():
        t += margen + f'{VERDE}{k.capitalize()}{RESET}\n'
        for v in seccion[k]:
            t += margen + f'{v} : {CELESTE}{seccion[k][v]}{RESET}\n'
        t+= '\n'     
            
    print2(t)
    

def crear_tabla(**kwargs):
    tabla = Table(expand=True,)
    tabla.add_column('servicio',justify='center')
    tabla.add_column('estado',justify='center')

    with Live(tabla):
        for servicio,estado in kwargs.items():
            tabla.add_row(servicio.capitalize(),str(estado).upper())
            time.sleep(0.5)

def tabla_versiones(versiones : list): 

    # versiones = [ (version, numero) ]

    tabla = Table(expand=True)
    tabla.add_column('version',justify='center')
    tabla.add_column('servers indexados',justify='center',style='magenta')
    for version, cantidad in versiones:

        tabla.add_row(version,str(cantidad))

    consola.print(tabla)



# probablemente lo modifique varias veces hasta encontrar la forma mas eficiente
limpiar = lambda : subprocess.run(cmd,shell=True,stderr=open(os.devnull,'w'))
      

def info_server(cuerpo : str,titulo : str =''):
    msg = f'''\n
# {titulo}

{cuerpo}

'''
    md = Markdown(msg)
    consola.print(md)



def pagina(n_pagina : int):
    etiqueta = f'# Pagina {n_pagina}'
    consola.print(Markdown(etiqueta,style='white'),style=configuracion.COLOR)