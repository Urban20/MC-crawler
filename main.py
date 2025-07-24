from mcserver import  *
from data import *


def leer_tag():
    with open('tags.txt','r') as tags:
        for tag in tags:
            yield tag

def servers_online(tag):
    bot = Crawler(tag=tag)
    for ip in bot.info():
        server = McServer(ip=ip)
        if server.obtener_data() == 'online':
            print(server)

def main():
    tags = leer_tag()
    for tag in tags:
        servers_online(tag=tag)
       
main()