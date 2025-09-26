from ui import empaquetar,VERSION
from db import conec
from colorama import init

init()
VIOLETA = '\033[0;95m'
RESET = '\033[0m '
FONDO_V = '\033[0;105m'
AMARILLO = '\033[0;33m'


# AUTOR: Urb@n - Matias Urbaneja
# USO RESPONSABLE: Este programa realiza escaneos de direcciones IP y puede generar tráfico elevado.
# RECOMIENDO NO ABUSAR DE LOS ESCANEOS.
# NOTA : El antivirus puede bloquear el funcionamiento o marcarlo como falso positivo.


LOGO = f'''   *           '     *
                  *   '            '  *          *
      _______----_______                          '       *   
°'==(______( o_(_____( ;)            *    '          '
           /|\\                *         *  
          / | \\    {VIOLETA}MC-Crawler {VERSION}{RESET}   *   '    *               
         /  |  \\   buscador de servers de Minecraft java           
        /   |   \\      *                        '          *
       /    |    \\   {FONDO_V}Escrito por => Urb@n{RESET}
       
github : https://github.com/Urban20
'''
ADVERTENCIA = f'{AMARILLO}\n[!] advertencia: El antivirus puede bloquear el correcto funcionamiento del programa y/o dar falsos positivos\n{RESET}'

if __name__ == '__main__': 
    try:
        print(LOGO)
        print(ADVERTENCIA)
        empaquetar()
        conec.close()            
    except Exception as e:
        print(f'\nhubo un problema: {e}')