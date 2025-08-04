'modulo puente entre la base de datos y el programa'

from data import *
from mcserver import  *
import db

tags_info = 'tags.txt'
servers = 'servers.data'


def mostrar(lista,version=None,porversion = True):
    'muestra los server cuando se buscan por version o pais'
    for ip in lista:
        IP = ip.split(':')[0]
        puerto = ip.split(':')[1]
        server = McServer(ip=IP,puerto=puerto)
        data = server.obtener_data()
        if porversion:
            if data == 'online' and re.search(version,server.info[2]): # doble filtrado
                print(server)
        else: # por pais
            if data == 'online':
                print(server)


def leer_tag():
    'funcion que lee los tags (palabras clave) y los retorna'
    try:
        with open(tags_info,'r') as tags:
            for tag in tags:
                yield tag

    except FileNotFoundError:
        print('\nno se encontraron los tags ...\n')

def servers_online(tag : str):
    'imprime los servidores que encuentre online'
    bot = Crawler(tag=tag)
    for ip,pais in bot.info():
        server = McServer(ip=ip,puerto=25565,pais=pais)

        if server.obtener_data() == 'online':
            print(server)
            db.insertar(dato=server.info)
            

def Buscar_Servers():
    'llama a las funciones necesarias para iniciar la busqueda de servers (busqueda de rstreo, no busqueda en db)'
    print('\n[#] rastreando servers de minecraft java, esto va a llevar tiempo ...\n')
    tags = leer_tag()
    for tag in tags:
        servers_online(tag=tag)
    


