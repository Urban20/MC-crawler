'modulo puente entre la base de datos y el programa'

from data import *
from mcserver import  *
import db
from os import remove
import ui 

tags_info = 'tags.txt'


def archivo(server,fecha,arch : str):
    'archivo temporal que retiene los servers filtrados para una mejor lectura'
    
    with open(arch,'a',encoding='utf-8') as sv:
        info = f'''
        \n
        {server.direccion}|
        veredicto {server.veredicto}
        motd {server.motd.replace('\n','')} | 
        version {server.version} | 
        jugadores {server.p_data}
        registrado el {fecha}\n'''
        sv.write(info)
                
def mostrar(lista : list,version=None,porversion = True):
    'muestra los server cuando se buscan por version o pais (estan en la db)'

    
    contador = 0 # contador de servidores por pagina
    n_pagina = 1 
    LIMITE = 10 # limite de servers por pagina

    arch = 'filtrados.txt' # archivos donde se guardan los servers filtrados temporales

    try:
        remove(arch)
        
    except FileNotFoundError: ...


    for elem in lista:
        IP = elem[0].split(':')[0]
        puerto = elem[0].split(':')[1]
        pais = elem[1]
        fecha = elem[2]
        server = McServer(ip=IP,puerto=puerto,pais=pais,fecha_otorgada=fecha)
        data = server.obtener_data()
        server.verificar_crackeado()

        if porversion:
            if data == 'online' and re.search(version,server.info[2]): # doble filtrado
                print(server)
                archivo(server=server,fecha=fecha,arch=arch)
                contador+=1
        else: # por pais
            if data == 'online':
                print(server)
                archivo(server=server,fecha=fecha,arch=arch)
                contador+=1


        if contador >= LIMITE:
            ui.interfaz.bloqueada = True
            ui.interfaz.actualizar_estado()
            entrada = str(input('[1] siguiente pagina >> ')).strip()
            if entrada == '1':
                n_pagina+=1
                print(f'\033[0;105m\n------------------\npagina numero: {n_pagina}\n------------------\n\033[0m')
                contador = 0
                
            else:
                ui.interfaz.bloqueada = False
                ui.interfaz.actualizar_estado()
                break
    ui.interfaz.bloqueada = False
    ui.interfaz.actualizar_estado()

            

def leer_tag():
    'funcion que lee los tags (palabras clave) y los retorna'
    try:
        with open(tags_info,'r') as tags:
            for tag in tags:
                yield tag

    except FileNotFoundError:
        print('\nno se encontraron los tags ...\n')

def servers_online(tag : str):
    'imprime los servidores que encuentre online por crawling'
    bot = Crawler(tag=tag)
    for ip,pais in bot.info():
        if pais == None:
            server = McServer(ip=ip,puerto=25565)
        else:
            server = McServer(ip=ip,puerto=25565,pais=pais)

        if server.obtener_data() == 'online':
            server.verificar_crackeado()
            try:
                db.insertar(dato=server.info)
                print(server)
            except: ...
            

def Buscar_Servers():
    'llama a las funciones necesarias para iniciar la busqueda de servers (busqueda de rstreo, no busqueda en db)'
    print('\n[#] rastreando servers de minecraft java, esto va a llevar tiempo ...\n')
    tags = leer_tag()
    for tag in tags:
        servers_online(tag=tag)
    


