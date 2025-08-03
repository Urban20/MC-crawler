# pequeño script que comunica go con python
# barre bloques de ips para detectar puertos abiertos de interes

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

    'automatiza la ejecucion del ejecutable de go'
    try:
        dir = os.getcwd()
        
        print('\n[+] barriendo bloques de ips, esto puede llevar tiempo ...\n ')
        print('NO cierres el programa')
        for n0,n1 in [(130,61),(54,36),(14,178),(151,80)]:
            com = subprocess.Popen([BINARIO,'-n0',str(n0),'-n1',str(n1),'-hl',str(HILOS)],shell=True)
        com.wait()

        print('\n[+] finalizado\n')
    except Exception as e:
        print(f'\nhubo un problema al ejecutar el binario: {e}\n')


def leer_stdout():
    
    try:
        with open(STDOUT,'r') as ips:
            for ip in ips:
                yield ip
    except Exception as e:
        print('\n no se pudo leer el archivo de salida\n')


def ejecutar_barrido():
    ejecutar_bin()
    for linea in leer_stdout():
        bot = McServer(ip=linea.replace('\n',''),puerto=25565)
        if bot.obtener_data() == 'online':
            print(bot)
            insertar(bot.info)
    os.remove(STDOUT)