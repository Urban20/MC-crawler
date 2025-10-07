import requests
import re
import random



def obtener_bloque_web(url : str,regex : str = r'(\d+)\.(\d+)\.0\.0'):
    try:
        LIMITE = 10
        user_ag ={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        }

        web = requests.get(url,headers=user_ag)

        if web.status_code == 200:
            rangos = re.findall(regex,web.text)

            print('\n[+] rangos obtenidos\n')
            
            return random.sample(rangos,k=min(len(rangos),LIMITE))
        
        else: 
            raise ConnectionError

    except (requests.ConnectionError,requests.ConnectTimeout) as e:
        print(f'\n[+] no se pudo obtener el rango ip: {e}\n')
        return []   
