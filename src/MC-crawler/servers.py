'''modulo puente entre la base de datos y el programa

provee funciones relacionadas directamente con la busqueda de servidores '''

from cidr_.data import *
from clases.mcserver import  *
from sqlite3 import DatabaseError,IntegrityError
from os import remove
from db import db
import sys
from utilidades import consola
from configuracion import configuracion
import shutil


arch = configuracion.FILTRADOS # archivos donde se guardan los servers filtrados temporales

def iniciar_busqueda(crackeados : bool = False):
    'imprime la busqueda de servidores de forma artistica'
    consola.limpiar(logo=False)
    x,_ = shutil.get_terminal_size()

    n_globales,n_crackeados = db.contar_indexados()

    logo=r'''
▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
▐ __  __                 ____                    _           ▌
▐|  \/  | ___           / ___|_ __ __ ___      _| | ___ _ __ ▌
▐| |\/| |/ __|  _____  | |   | '__/ _` \ \ /\ / / |/ _ \ '__|▌
▐| |  | | (__  |_____| | |___| | | (_| |\ V  V /| |  __/ |   ▌
▐|_|  |_|\___|          \____|_|  \__,_| \_/\_/ |_|\___|_|   ▌
▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌
     '''
    for linea in logo.strip().splitlines():
        print(linea.center(x))  
    print(consola.NEGRITA+'Busqueda NO premium'.center(x)+consola.RESET if crackeados else consola.NEGRITA+'Busqueda global'.center(x)+consola.RESET)

    print(f'servidores no premium indexados: {n_crackeados}'.center(x) if crackeados else f'servidores totales indexados: {n_globales}'.center(x))
    for _ in range(2):
        print('_'*x+'\n')  

    return str(input(consola.NEGRITA+'Buscar version >> '+consola.RESET)).strip()

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


def imprimir_servers(contador : int ,crackeados : bool,tupla,server : McServer):

    'funcion auxiliar llamada por funcion mostrar()'

    if crackeados:
        version_db = tupla[1]

        if version_db == server.version and server.veredicto != server.ET_PREM:
            # la db no premium solo mantiene los servers que ademas de estar onlines
            # coinciden con la version solicitada por el usuario
            # si la version cambia, automaticamente se cuenta como un server nuevo 
            # y se reevalua si entra dentro de la categoria no premium
            server.print()
            contador+=1
            
        else:
            db.eliminar_server(server.direccion)
            
    else:
        server.print()
        contador+=1

    return contador


def paginado(contador : int, limite : int, n_pagina :int):

    'funcion auxiliar de mostrar()'
    
    if contador < limite:
        return (contador,n_pagina,False)

    

    if str(input('siguiente pagina (s/n) >> ')).lower().strip() == 's':
        n_pagina+=1
        consola.pagina(n_pagina)
        return (0,n_pagina,False)
            
    return (contador,n_pagina,True)    



def mostrar(lista : list,version=None,porversion : bool = True,crackeados : bool = False):
    'maneja la logica de muestreo y paginado de los servers cuando se buscan desde las dbs'

    
    contador = 0 # contador de servidores por pagina
    LIMITE = 10 # limite de servers por pagina
    n_pagina = 1

    try:
        remove(arch)
        
    except FileNotFoundError: ...

    for tupla in lista:
        IP = tupla[0].split(':')[0]
        puerto = tupla[0].split(':')[1]
        fecha = tupla[-1]

        server = McServer(ip=IP,puerto=puerto,fecha_otorgada=fecha)
        data = server.obtener_data()
        server.verificar_crackeado()

        # registra los servers que se van mostrando en consola en tiempo real
        if not crackeados:
            registrar_crackeado(server=server)
                     
        if data == 'online' and re.search(version,server.info[2]): # doble filtrado
            

            # mostrar servidor dependiendo de la db que se consulte
            contador = imprimir_servers(crackeados=crackeados,
                             tupla=tupla,
                             server=server,
                             contador=contador)
                
            archivo(server=server,fecha=fecha,arch=arch)
        elif data == 'offline': 
            # para servers offlines, dependiendo que db se este consultando
            # la funcion de eliminacion varia ligeramente

            db.eliminar_server(server.direccion) if crackeados else db.eliminar_server(server.direccion,
                                                                                        conex=db.conec,
                                                                                        tabla=db.TABLA)
         
        else: # si el server no esta offline pero tampoco coincide con el doble filtrado
              # se verifica una posible cambio en la version para la db global
            if not crackeados:
                db.verificar_actualizacion(server,mostrar_sv=False)                   

        # paginado -----------------------------------------
        #  esta seccion detiene el muestreo cada cierto limite y pregunta si deseas continuar
        contador,n_pagina,detener = paginado(contador=contador,
                                               limite=LIMITE,
                                               n_pagina=n_pagina)
        if detener:
            return
        # paginado -----------------------------------------
    
servers_encontrados = 0 # cuenta los servers encontrados
# se muestra en consola en procesar_lineas() en gopython.py
def registrar_server(server : McServer):
    'esta funcion recicla la logica para insertar el server en db de servers historicos (todos) e imprimirlo'
    global servers_encontrados
    try:
        if server.info != None:
            db.insertar(dato=server.info)
            server.print()
            servers_encontrados+=1

    except IntegrityError:
        db.verificar_actualizacion(server) # verifica actualizacion de db global
        

    except DatabaseError as e:
        print(f'\n[!] error en la db : {e}\n')
        sys.exit(1)

def registrar_crackeado(server : McServer):
    'guarda server en base de datos de no premium si efectivamente lo es'
    if server.crackeado:
        # insertar en la tabla de los no premium (crackeados)
        try:
            db.insertar(espacios='(?,?,?)',
                        tabla=db.TABLA2,
                        cursor=db.cursor2,
                        dato=(server.direccion,server.version,server.fecha),
                        conex=db.conec2)
            
        except IntegrityError:
            ...            
            


    


