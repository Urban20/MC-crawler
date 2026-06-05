import socket
from utilidades.consola import log


def conectividad():
    
    for p in (53,443):

        log.debug(f'verificando conectividad en el puerto {p}')
 
        with socket.socket() as s:

            s.settimeout(5)

            if s.connect_ex(('8.8.8.8',p)) == 0:
                
                return True
        
    return False