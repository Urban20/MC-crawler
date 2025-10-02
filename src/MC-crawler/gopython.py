'''pequeño script que comunica go con python
barre bloques de ips para detectar puertos abiertos de interes'''

import subprocess
import os
from mcserver import McServer
import servers
import data

# 130 61
# 54.36.0.0/14 178.32.0.0/15 151.80.0.0/16

STDOUT = 'ip_escan.data' # no modificar 
TIMEOUT = 0.6

# para HILOS:
#  cuidado con subir demasiado este numero,
#  puede saturar tu equipo, ancho de banda
#  y simular un ataque D.O.S (no es la idea)
#  a mayor numero, mayor velocidad de escaneo pero mayor riesgo
HILOS = 50 

BINARIO = './escan'

ORACLE = 'https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json'
AMAZON = 'https://ip-ranges.amazonaws.com/ip-ranges.json'

BLOQUES24 = [(64,94,92),(74,112,76),(74,117,200),(199,195,140)]

def ejecutar_bin():
    'automatiza la ejecucion del bin de go'

    rango1 = data.obtener_bloque_web(ORACLE)
    rango2 = data.obtener_bloque_web(AMAZON)
    bloques = rango1 + rango2

    if bloques:
        print('\n[+] utilizando bloques web\n')
        BLOQUES16 = bloques
    else:
        BLOQUES16= [(130,61),(54,36),(14,178),(151,80),(50,20),(149,88),
            (54,38),(116,202),(116,203),(136,243),(66,179),(66,248),
            (63,135),(188,34),(188,40),(162,33),(173,240),(15,204),(51,81)
            ,(135,148)] 

    try:
        
        # para /24

        for n0,n1,n2 in BLOQUES24:
            subprocess.Popen([BINARIO,'-n0',str(n0),'-n1',str(n1),'-n2',str(n2),'-hl',str(HILOS),'-b24']).wait()
        

        for n0,n1 in BLOQUES16: # parametros para barrido de /16
            com1 = subprocess.Popen([BINARIO,'-n0',str(n0),'-n1',str(n1),'-hl',str(HILOS)])
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
        bot = McServer(ip=linea.replace('\n',''),timeout=TIMEOUT)
        if bot.obtener_data() == 'online':
            bot.verificar_crackeado()

            servers.registrar_server(server=bot)
            servers.registrar_crackeado(server=bot)
    print(f'\nservidores nuevos encontrados: {servers.servers_encontrados}')        
            


def ejecutar_barrido():

    try:
        os.remove(STDOUT)
    except FileNotFoundError: ...

    if servers.conectividad():
        print('\n[+] barriendo bloques de ips, esto puede llevar tiempo ...\n ')
        print('NO cierres el programa')
        ejecutar_bin()
        print('\n[+] barrido finalizado\nhaciendo ping a los servidores ...\n')
        procesar_lineas()
        
        