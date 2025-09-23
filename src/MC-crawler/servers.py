'modulo puente entre la base de datos y el programa'

from data import *
from mcserver import  *
from sqlite3 import DatabaseError,IntegrityError
from os import remove
import db
import ui 
from ping3 import ping

tags_info = 'tags.txt'

def conectividad():
    'funcion que verifica si hay conexion a internet haciendo ping al dns de google'
    try:
        timeout = 3
        return ping('8.8.8.8',timeout=timeout) != None
    except Exception: 
        print('\n[-] sin conexion o conexion debil\n')
        return False


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

def mostrar(lista : list,version=None,porversion : bool = True,crackeados : bool = False):
    'muestra los server cuando se buscan por version o pais (estan en la db)'

    
    contador = 0 # contador de servidores por pagina
    LIMITE = 10 # limite de servers por pagina
    arch = 'filtrados.txt' # archivos donde se guardan los servers filtrados temporales
    n_pagina = 1

    try:
        remove(arch)
        
    except FileNotFoundError: ...

    for tupla in lista:
        IP = tupla[0].split(':')[0]
        puerto = tupla[0].split(':')[1]
        fecha = tupla[-1]

        if crackeados:

            server = McServer(ip=IP,puerto=puerto,fecha_otorgada=fecha)

        else:  
            pais = tupla[1]      
            server = McServer(ip=IP,puerto=puerto,pais=pais,fecha_otorgada=fecha)
        
            

        data = server.obtener_data()
        server.verificar_crackeado()
        registrar_crackeado(server=server)

        if crackeados:
            print(server)

        elif porversion:
            if data == 'online' and re.search(version,server.info[2]): # doble filtrado
                print(server)
                archivo(server=server,fecha=fecha,arch=arch)
                
        else: # por pais
            if data == 'online':
                print(server)
                archivo(server=server,fecha=fecha,arch=arch)

        contador+=1     

        # paginado -----------------------------------------
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
        # paginado -----------------------------------------
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


def registrar_server(server : McServer):
    'esta funcion recicla la logica para insertar el server en db de servers historicos (todos) e imprimirlo'
    try:
        db.insertar(dato=server.info)
        print(server)

    except IntegrityError:
        ...
    except DatabaseError as e:
        print(f'\n[!] error en la db : {e}\n')
        sys.exit(1)

def registrar_crackeado(server : McServer):
    'guarda server en base de datos de no premium si efectivamente lo es'
    if server.crackeado == 1:
        # insertar en la tabla de los no premium (crackeados)
        try:
            db.insertar(espacios='(?,?,?)',
                        tabla=db.TABLA2,
                        cursor=db.cursor2,
                        dato=(server.direccion,server.version,server.fecha),
                        conex=db.conec2)
            
        except IntegrityError:
            ...            
            

def servers_online(tag : str):
    'imprime los servidores que encuentre online por crawling'
    bot = Crawler(tag=tag)
    for ip,pais in bot.info():
        if pais == None:
            servermc = McServer(ip=ip,puerto=25565)
        else:
            servermc = McServer(ip=ip,puerto=25565,pais=pais)

        if servermc.obtener_data() == 'online':
            servermc.verificar_crackeado()
            registrar_server(server=servermc)
            registrar_crackeado(server=servermc)


def Buscar_Servers():
    'llama a las funciones necesarias para iniciar la busqueda de servers (busqueda de rstreo, no busqueda en db)'
    if conectividad():
        print('\n[#] rastreando servers de minecraft java, esto va a llevar tiempo ...\n')
        tags = leer_tag()
        for tag in tags:
            servers_online(tag=tag)
    


