# scraper de servidores de minecraft - base de datos externa

import requests
import re
from bs4 import BeautifulSoup


class Crawler():
    def __init__(self,tag):
        self.tag = tag
        self.url = 'https://www.shodan.io/search?query='
        self.servers = []
        self.ips = []

    def info(self):
        web = requests.get(self.url+self.tag)
        if web.status_code == 200:
            try:
                html = BeautifulSoup(web.text,"html.parser")
                self.ips = html.find_all('a',class_='title text-dark')
                
            except:
                print('error de obtencion de ips')

            finally:
                for ip in self.ips:
                    yield ip.text

    

