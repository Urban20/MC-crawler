'''pequeño script que comunica go con python
barre bloques de ips para detectar puertos abiertos de interes'''

import subprocess
from utilidades import consola
import os
from clases.mcserver import McServer
import servers
from cidr_ import data
from configuracion import configuracion
import datetime
import clases.interruptor
from clases.contador import contador
import time

TIMEOUT = configuracion.TIMEOUT
TIMEOUT_ESCAN = configuracion.ESCAN_TIMEOUT
# para HILOS:
#  cuidado con subir demasiado este numero,
#  puede saturar tu equipo, ancho de banda
#  y simular un ataque D.O.S (no es la idea)
#  a mayor numero, mayor velocidad de escaneo pero mayor riesgo
HILOS = configuracion.HILOS

BINARIO = 'escan' # no modificar
CARPETA_BIN = 'binario'

ruta = os.path.join(os.path.dirname(__file__),CARPETA_BIN,BINARIO) # el binario debe estar en la misma ruta que este modulo
# ruta: es la ruta que se usa para ejecutar el binario

ORACLE = 'https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json'
AMAZON = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
GOOGLE = 'https://www.gstatic.com/ipranges/cloud.json'
HETZNER = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS24940'

regex16 = r'(\d+)\.(\d+)\.0\.0/16$'
regex24 = r'(\d+)\.(\d+)\.(\d+)\.0/24$'
interrupcion = clases.interruptor.Interruptor(evento='barrido') # objeto creado para barridos y barridos personalizados


def introducir_parametros(param1 : int ,param2 : int,param3 : int = 0,bits24 : bool = False):
    'introduce parametros especificos en el binario'

    parametros = [ruta,'-n0',str(param1),'-n1',str(param2),'-n2',str(param3),'-hl',str(HILOS),'-t',str(TIMEOUT_ESCAN)]
    
    if bits24:
        parametros.append('-b24')

    sp = subprocess.Popen(parametros,stdout=subprocess.PIPE)  
    procesar_lineas(subproc=sp)


def ejecutar_bin():
    '''automatiza la ejecucion del bin de go
    
    - obtiene los rangos de ip automaticamente'''
    rango1,estado1 = data.obtener_bloque_web(url=ORACLE)
    rango2,estado2 = data.obtener_bloque_web(url=AMAZON,regex=regex16)
    rango3,estado3 = data.obtener_bloque_web(url=GOOGLE,regex=regex16)
    rango4,estado4 = data.obtener_bloque_web(url=HETZNER,regex=regex16,limite=5)

    consola.crear_tabla([estado1,estado2,estado3,estado4])
    time.sleep(3)
    consola.limpiar()

    bloques = rango1 + rango2 + rango3 + rango4# bloques de rango web

    if bloques:
        print('\n[+] utilizando bloques web y predefinidos\n')

        BLOQUES16 = bloques + data.OTROS_random

    else:
        print('\n[+] utilizando solo bloques predefinidos\n')
        BLOQUES16 = data.OTROS
    try:

        interrupcion.iniciar()

        for n0,n1 in BLOQUES16: # parametros para barrido de /16

            if interrupcion.cancelado: # primera interrupcion de barrido
                                       # solo afecta a escaneos de barrido (no personalizados)
                break

            introducir_parametros(n0,n1)
            
        print('\n[+] finalizado\n')
    except Exception as e:
        print(f'\nhubo un problema al ejecutar el binario: {e}\n')


def procesar_lineas(subproc):
    for linea in subproc.stdout:
        try:

            if interrupcion.cancelado: # segunda interrupcion de barrido
                                       # utilizado en escaneos de barrido y escaneos personalizados
                break

            ip = linea.decode().replace('\n','').strip()
            server = McServer(ip=str(ip),
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

def ejecutar_barrido():

    print('\n[+] barriendo bloques de ips, esto puede llevar tiempo ...\n ')
    print('NO cierres el programa')
    ejecutar_bin()
    print(f'\nservidores nuevos encontrados: {contador.encontrados}\nservidores actualizados: {contador.actualizado}')
    contador.resetear() 
        
        