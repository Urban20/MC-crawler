'modulo que maneja la logica de la base de datos sqlite'

import sqlite3 as sq
import servers

conec = sq.connect('servers.db')
cursor = conec.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS servers(ip PRIMARY KEY,pais TEXT,version TEXT, fecha TEXT)')

def insertar(dato : tuple):
    try:
        cursor.execute('INSERT INTO servers VALUES(?,?,?,?)',dato)
        conec.commit()

    except Exception as e: print(f'error al insertar dato {e}')


def buscar_version(version : str):   
    'pide la version y devuelve las ips'

    print(f'\n[...] se muestra busqueda segun "{version}"\n')
    try:
        cursor.execute(f'SELECT ip FROM servers WHERE version LIKE ? ORDER BY fecha DESC',(f'%{version}',))
        ips = [ip[0] for ip in cursor] # ip:puerto
        servers.mostrar(ips,version)

    
    except Exception as e: print('error ',e)

def buscar_pais(pais : str):
    'pide el pais y devuelve las ips'

    print(f'\n[...] se muestra busqueda segun "{pais}"\n')
    try:
        cursor.execute(f'SELECT ip FROM servers WHERE pais = ? ORDER BY fecha DESC',(pais,))
        ips = [pais[0] for pais in cursor]
        servers.mostrar(ips,porversion=False)
    
    except Exception as e: print('error ',e)




