'''pequeño script que comunica go con python
barre bloques de ips para detectar puertos abiertos de interes'''

import subprocess
import os
from mcserver import McServer
from db import insertar


# 130 61
# 54.36.0.0/14 178.32.0.0/15 151.80.0.0/16

STDOUT = 'ip_escan.data' # no modificar 

# para HILOS:
#  cuidado con subir demasiado este numero,
#  puede saturar tu equipo, ancho de banda
#  y simular un ataque D.O.S (no es la idea)
#  a mayor numero, mayor velocidad de escaneo pero mayor riesgo
HILOS = 50 

BINARIO = 'escan.exe'


def ejecutar_bin():
    'automatiza la ejecucion del bin de go'

    try:
        os.getcwd()
        # para /24

        for n0,n1,n2 in [(149,88,39),(50,20,200),(50,20,248),(63,135,164),(64,94,92),(66,179,22),(66,179,218),
                        (66,248,192),(74,112,76),(74,117,200)]:
            subprocess.Popen([BINARIO,'-n0',str(n0),'-n1',str(n1),'-n2',str(n2),'-hl',str(HILOS),'-b24'],shell=True).wait()
        

        for n0,n1 in [(130,61),(54,36),(14,178),(151,80),(54,38),(116,202),(116,203),(136,243)]: # parametros para barrido de /16
            com1 = subprocess.Popen([BINARIO,'-n0',str(n0),'-n1',str(n1),'-hl',str(HILOS)],shell=True)
        com1.wait()

        print('\n[+] finalizado\n')
    except Exception as e:
        print(f'\nhubo un problema al ejecutar el binario: {e}\n')


def leer_stdout():
    
    try:
        with open(STDOUT,'r') as ips:
            for ip in ips:
                yield ip
    except:
        print('\n no se pudo leer el archivo de salida\n')

def procesar_lineas():
    for linea in leer_stdout():
        bot = McServer(ip=linea.replace('\n',''))
        if bot.obtener_data() == 'online':
            print(bot)
            insertar(bot.info)


def ejecutar_barrido():
    print('\n[+] barriendo bloques de ips, esto puede llevar tiempo ...\n ')
    print('NO cierres el programa')
    ejecutar_bin()
    procesar_lineas()
    
    os.remove(STDOUT)