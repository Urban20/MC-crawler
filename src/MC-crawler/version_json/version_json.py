import requests
import json
import db.db


JSON_VERSION = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
cache_versiones = []


def version_json():

    
    try:
        if cache_versiones:
            return []

        req = requests.get(JSON_VERSION)

        if req.status_code != 200:
            return
        
        dec = json.JSONDecoder()
        info = dec.decode(req.text)

        return list(info['versions'])
    
    except:
        return []
    

def listar_versiones(versiones : list):

    if not versiones and cache_versiones:
        print('\n(+) revisando informacion cacheada\n')
        return cache_versiones

    

    for version in versiones:

        if version['type'] != 'release':
            continue

        cache_versiones.append(version['id'])

    return cache_versiones    

def obtener_releases():
   
    return listar_versiones(version_json())


def contar_servidores():

    releases = obtener_releases()

    version_conteo = []

    if releases is None:
        print('\nno se pudo obtener informacion del conteo de servidores\n')
        return

    print('numeros de servidores clasificados por version:\n')

    for release in releases:

        n = db.db.contar_version(release)
        version_conteo.append((release,n))
    
    return version_conteo

