import socket


def conectividad():
    for p in (53,443):
        s = socket.socket()
        s.settimeout(5)
        if s.connect_ex(('8.8.8.8',p)) == 0:
            s.close()
            return True
    
    return False