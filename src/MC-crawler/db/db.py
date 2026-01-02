'''modulo que maneja la logica de las bases de datos sqlite del programa:

- base de datos global (todos los servidores encontrados independientemente su configuracion)

- base de datos de servidores no premium (base de datos secundaria)'''

import sqlite3 as sq
import servers
from clases.mcserver import McServer
import os
from utilidades.consola import ROJO,RESET
import configuracion.configuracion
from clases.interruptor import Interruptor
from clases.contador import contador

ruta_db = os.path.dirname(__file__)
# este modulo maneja dos bases de datos:
# por un lado, la base de datos general donde estan TODOS los servidores
# por el otro , se guardan servidores no premium (base de datos mas volatil y a corto plazo)

# base de datos principal (todos los servers):
DB = 'servers.db'
TABLA = 'servers'

# base de datos secundaria (solo los posibles crackeados):
DB2 = 'crackeados.db'
TABLA2 = 'server_np'

# tabla principal de serves historicos (todos)
conec = sq.connect(os.path.join(ruta_db,DB))
cursor = conec.cursor()
cursor.execute(f'CREATE TABLE IF NOT EXISTS {TABLA}(ip PRIMARY KEY,pais TEXT,version TEXT, fecha TEXT)')
# pais queda obsoleto en la db

def contar_indexados():
    contados1 = conec.cursor()
    contados2 = conec2.cursor()

    n_globales = int(contados1.execute(f'SELECT COUNT(*) FROM {TABLA}').fetchone()[0])
    n_crackeados = int(contados2.execute(f'SELECT COUNT(*) from {TABLA2}').fetchone()[0])
    return (n_globales,n_crackeados)

# tabla a la db de servers crackeados
conec2 = sq.connect(os.path.join(ruta_db,DB2))
cursor2 = conec2.cursor()
cursor2.execute(f'CREATE TABLE IF NOT EXISTS {TABLA2}(ip PRIMARY KEY, VERSION TEXT,FECHA TEXT)')


def actualizar_server(sv : McServer, ip_puerto,tabla = TABLA,conex = conec):
    'funcion simple que abstrae el comando de sqlite para actualizar servidores'
    actualizador = conex.cursor()
    actualizador.execute(f'UPDATE {tabla} SET version = ?, fecha = ? WHERE ip = ?', 
                                (sv.version, sv.fecha, ip_puerto))
    conex.commit()

def verificar_actualizacion(server : McServer, mostrar_sv : bool = True,tabla = TABLA,conex = conec):
    'esta funcion verifica actualizaciones'

    actualizar = conex.cursor()
    server_db = actualizar.execute(f'SELECT version FROM {tabla} WHERE ip = ?',(server.direccion,))
    version_db = server_db.fetchone()[0]
    
    if server.estado == 'online' and server.version != version_db:

        actualizar_server(sv=server,ip_puerto=server.direccion,conex=conex)
        print(f'\n{server.direccion} fue actualizado\nversion {version_db} → {server.version}\n')
        contador.incrementar_actualizados()
        if mostrar_sv:
            server.print()


def eliminar_server(direccion : str,conex = conec2,tabla = TABLA2):
    eliminar = conex.cursor()
    eliminar.execute(f'DELETE FROM {tabla} WHERE ip = ?',(direccion,))
    conex.commit()
    if tabla == TABLA2:
        print(f'{ROJO}{direccion} eliminado de db no-premium (offline/cambio de version/cambio a premium){RESET}')
    else:
        print(f'{ROJO}{direccion} eliminado de la base de datos global (offline){RESET}')

def purgar():
    '''funcion que borra servers que esten offline cuando el usuario da la orden
    
    purga la base de datos principal (todos los servers)'''
   
    try:
        
        borrados = 0
        actualizados = 0

        print('\n[...] iniciando purga de servidores\nNO cierres el programa\n')
        selector = conec.cursor() # nuevo cursor que selecciona e itera
        selector.execute(f"SELECT ip, version, fecha FROM {TABLA} WHERE fecha <= date('now','-30 days')")

        inter = Interruptor(evento='purgado')
        inter.iniciar()

        for datos in selector:

            if inter.cancelado:
                break
            
            ipv4 = datos[0].split(':')[0]
            puerto = datos[0].split(':')[1]
            version_db = datos[1]
            ip_puerto = datos[0]
            fecha_db = datos[2]
            sv = McServer(ip=ipv4,
                          puerto=puerto,
                          timeout=configuracion.configuracion.TIMEOUT_PURGADO)
            
            sv.obtener_data(reintentos=configuracion.configuracion.REINTENTOS)

            if sv.estado == 'offline':
                eliminar_server(conex=conec,
                                tabla=TABLA,
                                direccion=ip_puerto)
                borrados+=1
                    
            elif sv.version != version_db:
                # actualizador de la funcion purgar, no confundir con verificar_actualizacion()
                sv.verificar_crackeado()
                actualizar_server(sv=sv,ip_puerto=ip_puerto)
                servers.registrar_crackeado(sv)
                print(f'[↑] ACTUALIZADO: {ip_puerto} | version ({version_db} → {sv.version}) | {fecha_db} → {sv.fecha}')
                actualizados+=1
            
                
            
        print(f'\npurga finalizada\nservers eliminados (offlines): {borrados} | servers actualizados: {actualizados}\n')
    except Exception as e:
        print(f'\n[-] hubo un problema al intentar purgar la db\n{e}')
 
def insertar(dato : tuple,espacios :str = '(?,?,?,?)',tabla :str = TABLA,cursor = cursor,conex = conec):
    
    'inserta valores en las bases de datos que se le asigne'

    cursor.execute(f'INSERT INTO {tabla} VALUES{espacios}',dato)
    conex.commit()


def buscar_version(version : str):   
    'pide la version y devuelve las ips'
    
    print(f'\n[...] se muestra busqueda segun "{version}"\n')
    try:
        cursor.execute(f'SELECT ip,fecha FROM {TABLA} WHERE version LIKE ? ORDER BY fecha DESC',(f'%{version}',))
        
        servers.mostrar(lista=cursor,version=version)

    
    except : ...


def buscar_crackeados(version : str):
    'itera con los servers que determine como no premium'
    
    print(f'\n[...] se muestra busqueda de posible servers no premium')
    try:
        cursor2.execute(f'SELECT ip,VERSION,FECHA FROM {TABLA2} WHERE version LIKE ? ORDER BY FECHA DESC',(f'%{version}',))

        servers.mostrar(lista=cursor2,crackeados=True,version=version)
    
    except : ...



