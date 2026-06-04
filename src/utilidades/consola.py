from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.live import Live
import time
from rich.logging import RichHandler
from configuracion import configuracion
import subprocess
import os
import sys
import shutil
import logging

PROGRAMA = 'MC-Crawler'

consola = Console()

if len(sys.argv) == 2 and sys.argv[1] == '--debug':

    modo = logging.DEBUG
else:

    modo = logging.INFO

log = logging.getLogger(PROGRAMA)
logging.basicConfig(datefmt='[%X]',
                    level=modo,
                    handlers=[RichHandler(console=consola)],
                    format='%(message)s')



margen = ' ' * 2

NEGRITA = '\033[1m'
VERSION = 'V7.0' # version del programa
RESET = '\033[0m '
AMARILLO = '\033[0;33m'


cmd = 'cls' if os.name == 'nt' else 'clear'

def rgb(r,g,b, fondo : bool = False):

    d = 38

    if fondo:
        d = 48

    return f'\033[{d};2;{r};{g};{b}m'

GRIS_LOGO = rgb(227, 227, 227)
GRIS_OSCURO = rgb(51, 51, 51)
COLOR_PANEL_MENU = rgb(42, 30, 69,fondo=True)

LOGO = f'''
\033[1;35m{' '*10}██▄  ▄██  ▄▄▄▄     ▄█████ ▄▄▄▄   ▄▄▄  ▄▄   ▄▄ ▄▄    ▄▄▄▄▄ ▄▄▄▄  
\033[0;35m{' '*10}██ ▀▀ ██ ██▀▀▀ ▄▄▄ ██     ██▄█▄ ██▀██ ██ ▄ ██ ██    ██▄▄  ██▄█▄ 
\033[2;35m{' '*10}██    ██ ▀████     ▀█████ ██ ██ ██▀██  ▀█▀█▀  ██▄▄▄ ██▄▄▄ ██ ██ \n
{GRIS_LOGO}
{VERSION}
escrito por: Urb@n 
{RESET}                                                                                                                                                                                     
'''
# etiquetas que se muestran en la consola como veredicto de los servidores
ET_CRACK = 'crackeado/no premium'
ET_PREM = 'premium'
ET_IND = 'indeterminado'
ET_TIM = 'tiempo agotado'
ET_INC = 'protocolo incompatible'
ET_BAN = 'BANEADO'
ET_MOD = 'MODEADO'


def print_centro(txt : str):

    x,_ = shutil.get_terminal_size()

    print(txt.center(x))


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
    
    for linea in LOGO.splitlines():
        print_centro(linea)
        time.sleep(delay)

def ver_config():
    limpiar()

    t=''
    seccion = configuracion.config

    for k in seccion.sections():
        for v in seccion[k]:
            t += margen + f'{v.replace('_',' ').capitalize()} : {seccion[k][v]}\n'
                    
    box(t.splitlines(),margen=4)
    

def crear_tabla(**kwargs):
    tabla = Table(expand=True,)
    tabla.add_column('servicio',justify='center')
    tabla.add_column('estado',justify='center')

    with Live(tabla):
        for servicio,estado in kwargs.items():
            tabla.add_row(servicio.capitalize(),str(estado).upper())
            time.sleep(0.5)


# probablemente lo modifique varias veces hasta encontrar la forma mas eficiente
def limpiar():
    with open(os.devnull,'w') as devnull:
        subprocess.run(cmd,shell=True,stderr=devnull)
      

def info_server(cuerpo : str,titulo : str =''):
    msg = f'# {titulo}\n{cuerpo}'
    md = Markdown(msg,code_theme='paraiso-dark')
    consola.print(md)


def maximo(l : list[str]): 

    '''
    devuelve el numero maximo de caracteres de una lista de strings
    '''

    n = 0

    for elemento in l:

        long = len(elemento)

        if n < long:
            n = long

    return n



def box(opciones : list, color : str = COLOR_PANEL_MENU,margen : int = 10):


    m = maximo(opciones)
    margen_ansi = ' ' * len(color)

    borde1 = f'{margen_ansi}{color}┌{'─' * (m + margen)}┐{RESET}'
    borde2 = f'{margen_ansi}{color}└{'─' * (m + margen)}┘{RESET}'
    print('\n')
    print_centro(borde1)

    for op in opciones:

        print_centro(f'{margen_ansi}{color}│ {op}{' '* ((m + margen - 1) - len(op))}│{RESET}')
    
    print_centro(borde2)
    print('\n')
    
def pagina(n_pagina : int):
    
    box(f'Pagina {n_pagina}'.splitlines(),margen=2)