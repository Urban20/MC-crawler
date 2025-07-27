# scraper de servidores de minecraft - base de datos externa

import requests
import re

class Crawler():
    'la clase Crawler es la encargada de la obtencion de los datos'
    def __init__(self,tag):
        self.tag = tag
        self.url = 'https://www.shodan.io/search?query='
        self.servers = []
        self.ips = []

    def info(self):
        try:
            
            web = requests.get(self.url+self.tag,headers={'User-Agent': 'Mozilla/5.0'})
            if web.status_code == 200:
                
                self.ips = re.findall(r'/host/(\d+\.\d+\.\d+\.\d+)',web.text)
                    
                for ip in self.ips:
                    yield ip
        except Exception as e:
            print(f'hubo un problema al consultar los recursos: {e}')

