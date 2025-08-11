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
        cursor.execute('SELECT ip FROM servers')
        for ip in cursor:
            ipv4 = ip[0].split(':')[0]
            puerto = ip[0].split(':')[1]
            sv = McServer(ip=ipv4,puerto=puerto)
            if sv.obtener_data() == 'offline':
                cursor.execute('DELETE FROM servers WHERE ip = ?',ip)
                conec.commit()
                print(f'[-] server {ipv4} eliminado de la db')
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

    
    except Exception as e: print('error ',e)

def buscar_pais(pais : str):
    'pide el pais y devuelve las ips'

    print(f'\n[...] se muestra busqueda segun "{pais}"\n')
    try:
        cursor.execute(f'SELECT ip, pais, fecha FROM servers WHERE pais = ? ORDER BY fecha DESC',(pais,))

        servers.mostrar(cursor,porversion=False)
    
    except Exception as e: print('error ',e)




