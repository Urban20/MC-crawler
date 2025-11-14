import socket


def conectividad():
    s = socket.socket()
    s.settimeout(3)
    return s.connect_ex(('8.8.8.8',443)) == 0