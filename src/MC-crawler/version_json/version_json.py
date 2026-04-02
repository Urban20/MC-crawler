import requests
import json
import db.db
from clases.bot import versionado_viejo,n_ver


JSON_VERSION = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
cache_versiones = []


def version_json():

    
    try:
        if cache_versiones:
            return []

        req = requests.get(JSON_VERSION)

        if req.status_code != 200:
            return []
        
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

        version_str = version['id']

        if version['type'] != 'release' or (versionado_viejo(version_str) is True and n_ver(version_str) < 6):
            continue

        cache_versiones.append(version_str)

    return cache_versiones    

def obtener_releases():
   
    return listar_versiones(version_json())


def contar_servidores():

    releases = obtener_releases()

    version_conteo = []

    if releases is None:
        print('\nno se pudo obtener informacion del conteo de servidores\n')
        return

    print('\nnumeros de servidores clasificados por version:\n')

    for release in releases:

        n = db.db.contar_version(release)
        version_conteo.append((release,n))
    
    return version_conteo

