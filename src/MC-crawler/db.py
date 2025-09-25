'''modulo que maneja la logica de las bases de datos sqlite del programa:

- base de datos global (todos los servidores encontrados independientemente su configuracion)

- base de datos de servidores no premium (base de datos secundaria)'''

import sqlite3 as sq
import servers
from mcserver import McServer

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
conec = sq.connect(DB)
cursor = conec.cursor()
cursor.execute(f'CREATE TABLE IF NOT EXISTS {TABLA}(ip PRIMARY KEY,pais TEXT,version TEXT, fecha TEXT)')

# tabla a la db de servers crackeados
conec2 = sq.connect(DB2)
cursor2 = conec2.cursor()
cursor2.execute(f'CREATE TABLE IF NOT EXISTS {TABLA2}(ip PRIMARY KEY, VERSION TEXT,FECHA TEXT)')

def eliminar_crackeado(direccion : str):
    cursor2.execute(f'DELETE FROM {TABLA2} WHERE ip = ?',(direccion,))
    conec2.commit()
    print(f'\n{direccion} eliminado de db no-premium\n')

def purgar():
    '''funcion que borra servers que esten offline cuando el usuario da la orden
    
    purga la base de datos principal (todos los servers)'''
    
    if servers.conectividad():   
        try:
            borrados = 0
            actualizados = 0

            print('\n[...] iniciando purga de servidores\nNO cierres el programa\n')
            selector = conec.cursor() # nuevo cursor que selecciona e itera
            selector.execute(f"SELECT ip, version, fecha FROM {TABLA} WHERE fecha <= date('now','-30 days')")
            for datos in selector:
                
                ipv4 = datos[0].split(':')[0]
                puerto = datos[0].split(':')[1]
                version_db = datos[1]
                ip_puerto = datos[0]
                fecha_db = datos[2]
                sv = McServer(ip=ipv4,puerto=puerto)
                sv.obtener_data()

                if sv.estado == 'offline':
                    cursor.execute(f'DELETE FROM {TABLA} WHERE ip = ?',(ip_puerto,))
                    print(f'\033[0;31m[-] server {ipv4} eliminado de la db\033[0m')
                    borrados+=1

                elif sv.version != version_db:
                    sv.verificar_crackeado()
                    cursor.execute(f'UPDATE {TABLA} SET version = ?, fecha = ? WHERE ip = ?', 
                                (sv.version, sv.fecha, ip_puerto))
                    print(f'[↑] ACTUALIZADO: {ip_puerto} | version ({version_db} → {sv.version}) | {fecha_db} → {sv.fecha}')
                    actualizados+=1
                
                conec.commit()         
                
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
        cursor.execute(f'SELECT ip, pais, fecha FROM {TABLA} WHERE version LIKE ? ORDER BY fecha DESC',(f'%{version}',))
        
        servers.mostrar(lista=cursor,version=version)

    
    except : ...

def buscar_pais(pais : str):
    'pide el pais y devuelve las ips'
    
    print(f'\n[...] se muestra busqueda segun "{pais}"\n')
    try:
        cursor.execute(f'SELECT ip, pais, fecha FROM {TABLA} WHERE pais = ? ORDER BY fecha DESC',(pais,))

        servers.mostrar(lista=cursor,porversion=False)
    
    except : ...

def buscar_crackeados():
    'itera con los servers que determine como no premium'
    
    print(f'\n[...] se muestra busqueda de posible servers no premium')
    try:
        cursor2.execute(f'SELECT ip,VERSION,FECHA FROM {TABLA2} ORDER BY FECHA DESC')

        servers.mostrar(lista=cursor2,porversion=False,crackeados=True)
    
    except : ...



