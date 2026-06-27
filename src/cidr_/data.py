'modulo encargado de la obtencion de los rangos ip cuando se trata de escaneos automaticos'

import requests
import re
import random
from utilidades.consola import log

ORACLE = 'https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json'
AMAZON = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
GOOGLE = 'https://www.gstatic.com/ipranges/cloud.json'
HETZNER = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS24940'
OVH = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS16276'

# expresiones regulares utilizadas para extraer bloques, cubren los rangos de forma general
regex16 = r'(\d+)\.(\d+)\.0\.0/16' 
regex24 = r'(\d+)\.(\d+)\.(\d+)\.0/24'
regex8 = r'(\d+)\.0\.0\.0/8'

# otros bloques ip fijos
OTROS = [(130,61),(54,36),(14,178),(151,80),(50,20),(149,88),
      (54,38),(116,202),(116,203),(136,243),(66,179),(66,248),
      (63,135),(188,34),(188,40),(162,33),(173,240),(15,204),(51,81),
      (135,148)] 



def obtener_bloque_web(url : str,regex : str = r'(\d+)\.(\d+)\.0\.0',limite : int = 10,timeout = 5):
    try:
        log.debug(f'obteniendo informacion de {url}')

        with requests.get(url,timeout=timeout) as web:

            if web.status_code != 200:

                raise ConnectionError


            rangos = re.findall(regex,web.text)
            log.debug(f'{url} info obtenida')    
            return (random.sample(rangos,k=min(len(rangos),limite)),'ok')
        
        

    except Exception as e:

        log.debug(f'falla al obtener info de {url} | error: {e}')
        return ([],'fallo')   


if __name__ == '__main__':
    i = 0
    t = ''
    for url in (GOOGLE,AMAZON,ORACLE,HETZNER,OVH):
        bloque = obtener_bloque_web(url)
        t+= f'\nbloque {i}: {bloque}\n'
        i +=1
    print(t)