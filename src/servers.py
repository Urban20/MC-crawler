# modulo que se ocupa del manejo de archivos e informacion

from data import *
from mcserver import  *
import re
import os

tags_info = 'tags.txt'
servers = 'servers.data'

codif = 'utf-8'


def filtrar_info(regex : str):
    'filtra los servidores que coinciden con la busqueda y que estan online'
    contador = 0
    try:
        with open(servers,'r',encoding=codif) as sv:
            print(f'\n[#] lista de servidores que coinciden con "{regex}":\n')
            for linea in sv:

                if re.search(regex,linea.lower()):
                    ip = re.search(r'ip:\s+(\d+\.\d+\.\d+\.\d+):',linea).group(1)
                    puerto = re.search(r'ip:\s+\d+\.\d+\.\d+\.\d+:(\d+)',linea).group(1)
                    pais = re.search(r'pais:\s+([^|]+)',linea).group(1).strip()
                    server = McServer(ip=ip,puerto=int(puerto),pais=pais)
                    server.obtener_data()
                    print(server)
                    contador += 1
            print(f'\nservers encontrados: {contador}\n')
    except FileNotFoundError: 
        print('\nno se encontro el archivo\n')
    except Exception as e:
        print(f'hubo un problema al filtrar los servidores: {e}')
        
def eliminar_clones():
    with open(servers,'r',encoding=codif) as sv1:
        data = set(sv1)
    with open(servers,'w',encoding=codif) as sv2:
        sv2.writelines(data)
        
    
    
def guardar_sv(server : str):
    'guardado de servidores en formato utf-8'
    try:
        with open(servers,'a',encoding=codif) as temp:
            temp.write(server)

    except:
        print('server no guardado por un error\n')


def leer_tag():
    'funcion que lee los tags (palabras clave) y los retorna'
    with open(tags_info,'r') as tags:
        for tag in tags:
            yield tag


def servers_online(tag : str):
    'imprime los servidores que encuentre online'
    bot = Crawler(tag=tag)
    for ip,pais in bot.info():
        server = McServer(ip=ip,puerto=25565,pais=pais)

        if server.obtener_data() == 'online':
            print(server)
            guardar_sv(server=server.info)
            

def Buscar_Servers():
    'llama a las funciones necesarias para iniciar la busqueda de servers'
    print('\n[#] rastreando servers de minecraft java, esto va a llevar tiempo ...\n')
    tags = leer_tag()
    for tag in tags:
        servers_online(tag=tag)
    eliminar_clones()


