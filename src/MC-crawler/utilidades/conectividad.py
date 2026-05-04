import socket


def conectividad():
    
    for p in (53,443):
 
        with socket.socket() as s:

            s.settimeout(5)

            if s.connect_ex(('8.8.8.8',p)) == 0:
                
                return True
        
    return False