from mcserver import  *
from data import *


def guardar_sv(server : str):
    try:
        with open("servers.txt","a",encoding='utf-8') as sv:
            sv.write(server)
    except:
        print("server no guardado por un error\n")


def leer_tag():
    with open('tags.txt','r') as tags:
        for tag in tags:
            yield tag

def servers_online(tag):
    bot = Crawler(tag=tag)
    for ip in bot.info():
        server = McServer(ip=ip,puerto=25565)
        if server.obtener_data() == 'online':
            print(server)
            guardar_sv(server=server.info)
            

def main():
    tags = leer_tag()
    for tag in tags:
        servers_online(tag=tag)
       
if __name__ == '__main__':
    main()