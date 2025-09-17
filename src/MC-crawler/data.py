'scraper de servidores de minecraft - base de datos externa'

import requests
import re
import sys

class Crawler():
    'la clase Crawler es la encargada de la obtencion de los datos'

    '''
    aviso:
    Para volúmenes grandes de datos o mayor confiabilidad,
    se recomienda el uso de la API oficial de Shodan.
    NO abuses del scraping: se debe utilizar con cautela
    el codigo proporcionado NO esta pensado para scraping masivo
    ni solicitudes masivas.

    NO me hago responsable por el uso abusivo que se le pueda dar a esta
    funcionalidad.'''


    def __init__(self,tag):
        self.tag = tag
        self.url = 'https://www.shodan.io/search?query='  
        
    def info(self):
        try:
            
            web = requests.get(self.url+self.tag,headers={'User-Agent': 'Mozilla/5.0'})
            if web.status_code == 200:
                
                ips = re.findall(r'>(\d+\.\d+\.\d+\.\d+)<',web.text)
                paises = re.findall(r'title="([^"]+)[0-9A-Za-z"= ]+class="flag"',web.text)
                

                while len(paises) != len(ips):
                    paises.append(None)
                    
                for ip,pais in zip(ips,paises):
                    yield (ip,pais)
            else:
                print(f'\n[!] scraping no disponible\ncodigo de estado : {web.status_code}\n')
                sys.exit(0)

        except Exception as e:
            print(f'\nhubo un problema al consultar los recursos:\n{e}\n')

