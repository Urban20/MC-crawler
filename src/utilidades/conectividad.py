import socket
from utilidades.consola import log
import time
import sys


def conectividad():
    
    for p in (53,443):

        log.debug(f'verificando conectividad en el puerto {p}')
 
        with socket.socket() as s:

            s.settimeout(5)

            if s.connect_ex(('8.8.8.8',p)) == 0:
                
                return True
        
    return False


def verificar_conexion():

    if conectividad():

        return

    log.critical('se necesita conexion a internet para poder operar este programa')
    time.sleep(5)
    sys.exit(1)