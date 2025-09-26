'modulo puente entre la base de datos y el programa'

from data import *
from mcserver import  *
from sqlite3 import DatabaseError,IntegrityError
from os import remove
import db
import ui 
from ping3 import ping
import sys

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
    'maneja la logica de muestreo y paginado de los servers cuando se buscan desde las dbs'

    
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

        # registra los servers que se van mostrando en consola en tiempo real
        if not crackeados:
            registrar_crackeado(server=server)
            

        if crackeados:
            version_db = tupla[1]
            
            if data == 'online' and version_db == server.version:
                print(server)
            else:
                db.eliminar_crackeado(server.direccion)
                continue
        else:    
        
            if porversion and data == 'online' and re.search(version,server.info[2]):
                # doble filtrado
                print(server)
                   
                archivo(server=server,fecha=fecha,arch=arch)
                    
            else: # por pais
                if data == 'online':
                    print(server)
                      
                    archivo(server=server,fecha=fecha,arch=arch)
                                     
        contador+=1  

        # paginado -----------------------------------------
        #  esta seccion detiene el muestreo cada cierto limite y pregunta si deseas continuar
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
            


    


