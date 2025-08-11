'modulo que maneja la logica de la base de datos sqlite'

import sqlite3 as sq
import servers
from mcserver import McServer

conec = sq.connect('servers.db')
cursor = conec.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS servers(ip PRIMARY KEY,pais TEXT,version TEXT, fecha TEXT)')

def purgar():
    'funcion que borra servers que esten offline cuando el usuario da la orden'
    try:
        selector = conec.cursor() # nuevo cursor que selecciona e itera
        selector.execute('SELECT ip, version FROM servers')
        for datos in selector:
            try:
                ipv4 = datos[0].split(':')[0]
                puerto = datos[0].split(':')[1]
                version_db = datos[1]
                ip_puerto = datos[0]
                sv = McServer(ip=ipv4,puerto=puerto)
                sv.obtener_data()

                if sv.estado == 'offline':
                    cursor.execute('DELETE FROM servers WHERE ip = ?',(ip_puerto,))
                    print(f'\033[0;31m[-] server {ipv4} eliminado de la db\033[0m')

                elif sv.version != version_db:
                    cursor.execute('UPDATE servers SET version = ? WHERE ip = ?', 
                                (sv.version, ip_puerto))
                    print(f'[↑] ACTUALIZADO: {ip_puerto} | version ({version_db} → {sv.version})')
                
                else: 
                    print(f'\033[0;32m[✓] {ipv4} esta en orden\033[0m')
                
                conec.commit()

            except Exception as e:

                print(f'hubo un problema con {ipv4}: {e}')
                continue
            
            
        

    except Exception as e:
        print(f'\n[-] hubo un problema al intentar purgar la db\n{e}')
    
def insertar(dato : tuple):
    try:
        cursor.execute('INSERT INTO servers VALUES(?,?,?,?)',dato)
        conec.commit()

    except Exception as e: print(f'error al insertar dato {e}')


def buscar_version(version : str):   
    'pide la version y devuelve las ips'

    print(f'\n[...] se muestra busqueda segun "{version}"\n')
    try:
        cursor.execute(f'SELECT ip, pais, fecha FROM servers WHERE version LIKE ? ORDER BY fecha DESC',(f'%{version}',))
        
        servers.mostrar(cursor,version)

    
    except : ...

def buscar_pais(pais : str):
    'pide el pais y devuelve las ips'

    print(f'\n[...] se muestra busqueda segun "{pais}"\n')
    try:
        cursor.execute(f'SELECT ip, pais, fecha FROM servers WHERE pais = ? ORDER BY fecha DESC',(pais,))

        servers.mostrar(cursor,porversion=False)
    
    except : ...




