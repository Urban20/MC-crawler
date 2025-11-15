'''pequeño script que comunica go con python
barre bloques de ips para detectar puertos abiertos de interes'''

import subprocess
import consola
import os
from mcserver import McServer
import servers
import data
import configuracion
import datetime
import sys

STDOUT = 'ip_escan.data' # no modificar 
TIMEOUT = configuracion.TIMEOUT
TIMEOUT_ESCAN = configuracion.ESCAN_TIMEOUT
# para HILOS:
#  cuidado con subir demasiado este numero,
#  puede saturar tu equipo, ancho de banda
#  y simular un ataque D.O.S (no es la idea)
#  a mayor numero, mayor velocidad de escaneo pero mayor riesgo
HILOS = configuracion.HILOS

BINARIO = 'escan' # no modificar

ruta = os.path.join(os.path.dirname(__file__),BINARIO)

ORACLE = 'https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json'
AMAZON = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
GOOGLE = 'https://www.gstatic.com/ipranges/cloud.json'
HETZNER = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS24940'

def ejecutar_bin():
    'automatiza la ejecucion del bin de go'
    regex16 = r'(\d+)\.(\d+)\.0\.0/16'
    rango1,estado1 = data.obtener_bloque_web(url=ORACLE)
    rango2,estado2 = data.obtener_bloque_web(url=AMAZON,regex=regex16)
    rango3,estado3 = data.obtener_bloque_web(url=GOOGLE,regex=regex16)
    rango4,estado4 = data.obtener_bloque_web(url=HETZNER,regex=regex16,limite=5)

    consola.crear_tabla([estado1,estado2,estado3,estado4])

    bloques = rango1 + rango2 + rango3 + rango4# bloques de rango web

    if bloques:
        print('\n[+] utilizando bloques web y predefinidos\n')

        BLOQUES16 = bloques + data.OTROS_random

    else:
        print('\n[+] utilizando solo bloques predefinidos\n')
        BLOQUES16 = data.OTROS
    try:
    
        for n0,n1 in BLOQUES16: # parametros para barrido de /16
            sp = subprocess.Popen([ruta,'-n0',str(n0),'-n1',str(n1),'-hl',str(HILOS),'-t',str(TIMEOUT_ESCAN)],
                                  stdout=subprocess.PIPE)
            
            procesar_lineas(subproc=sp.stdout)

            sp.wait()


        print('\n[+] finalizado\n')
    except Exception as e:
        print(f'\nhubo un problema al ejecutar el binario: {e}\n')


def procesar_lineas(subproc):
    for linea in subproc:
        try:
            ip = str(linea.decode()).replace('\n','').strip()
            print(ip)
            server = McServer(ip=ip,
                timeout=TIMEOUT,
                # se muestra el tiempo actual a la hora de mostrar el servidor antes de insertar en la db
                fecha_otorgada=datetime.datetime.today().isoformat(sep=' ',timespec='seconds'
                ))
            
            if server.obtener_data() == 'online':
                server.verificar_crackeado()

            servers.registrar_server(server=server)
            servers.registrar_crackeado(server=server)

        except Exception as e:
            print(f'\n hubo un problema : {e}\n')
            

    print(f'\nservidores nuevos encontrados: {servers.servers_encontrados}')        
            


def ejecutar_barrido():

    try:
        os.remove(STDOUT)
    except FileNotFoundError: ...

    print('\n[+] barriendo bloques de ips, esto puede llevar tiempo ...\n ')
    print('NO cierres el programa')
    ejecutar_bin()
        
        