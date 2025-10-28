'modulo encargado de la obtencion de los rangos ip'
import requests
import re
import random

# otros bloques ip fijos
OTROS = [(130,61),(54,36),(14,178),(151,80),(50,20),(149,88),
      (54,38),(116,202),(116,203),(136,243),(66,179),(66,248),
      (63,135),(188,34),(188,40),(162,33),(173,240),(15,204),(51,81),
      (135,148)] 

OTROS_random = random.sample(OTROS,k=5)


def obtener_bloque_web(url : str,regex : str = r'(\d+)\.(\d+)\.0\.0',limite : int = 10):
    try:
        
        user_ag ={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        }

        web = requests.get(url,headers=user_ag)

        if web.status_code == 200:
            rangos = re.findall(regex,web.text)

            
            
            return (random.sample(rangos,k=min(len(rangos),limite)),'ok')
        
        else: 
            raise ConnectionError

    except (requests.ConnectionError,requests.ConnectTimeout) as e:
        
        return ([],'fallo')   
