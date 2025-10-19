'''modulo puente entre la base de datos y el programa

provee funciones relacionadas directamente con la busqueda de servidores y
conectividad del programa '''

from data import *
from mcserver import  *
from sqlite3 import DatabaseError,IntegrityError
from os import remove
import db
from ping3 import ping
import sys
import consola
import configuracion
import shutil


arch = configuracion.FILTRADOS # archivos donde se guardan los servers filtrados temporales

def iniciar_busqueda():
    'imprime la busqueda de servidores de forma artistica'
    consola.limpiar(logo=False)
    x,_ = shutil.get_terminal_size()

    logo=r'''
    ////////////////////////////////////////////////////////////
// __  __            ____                    _            //
//|  \/  | ___      / ___|_ __ __ ___      _| | ___ _ __  //
//| |\/| |/ __|____| |   | '__/ _` \ \ /\ / / |/ _ \ '__| //
//| |  | | (_|_____| |___| | | (_| |\ V  V /| |  __/ |    //
//|_|  |_|\___|     \____|_|  \__,_| \_/\_/ |_|\___|_|    //
////////////////////////////////////////////////////////////
     '''
    for linea in logo.strip().splitlines():
        print(linea.center(x))

    print(consola.NEGRITA+'Buscador de servidores.'.center(x)+consola.RESET)
    for _ in range(2):
        print('_'*x+'\n')
    return str(input(consola.NEGRITA+'Buscar version >> '+consola.RESET)).strip()

def conectividad():
    'funcion que verifica si hay conexion a internet haciendo ping al dns de google'
    try:
        timeout = 3
        if ping('8.8.8.8',timeout=timeout) == None:
            raise Exception
        return True
    except PermissionError:
        print('\n[-] se requieren privilegios elevados\n')
        return False
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
            

        if crackeados:
            version_db = tupla[1]
            
            if data == 'online' and version_db == server.version and server.veredicto != '\033[0;31mposiblemente premium\033[0m':
                server.print()
            else:
                db.eliminar_crackeado(server.direccion)
                continue
        else:    
            
            if porversion and data == 'online' and re.search(version,server.info[2]):
                # doble filtrado
                server.print()
                   
                archivo(server=server,fecha=fecha,arch=arch)
                    
            
                                     
        contador+=1  

        # paginado -----------------------------------------
        #  esta seccion detiene el muestreo cada cierto limite y pregunta si deseas continuar
        if contador >= LIMITE:

            entrada = str(input('[1] siguiente pagina >> ')).strip()
            if entrada == '1':
                n_pagina+=1
                consola.pagina(n_pagina)
                contador = 0
                
            else:
                

                break
        # paginado -----------------------------------------
    
servers_encontrados = 0 # cuenta los servers encontrados
# se muestra en consola en procesar_lineas() en gopython.py
def registrar_server(server : McServer):
    'esta funcion recicla la logica para insertar el server en db de servers historicos (todos) e imprimirlo'
    global servers_encontrados
    try:
        db.insertar(dato=server.info)
        server.print()
        servers_encontrados+=1

    except IntegrityError: # agregar para verificar server y comparar versiones
        db.verificar_actualizacion(server)
        

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
            


    


