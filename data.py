# scraper de servidores de minecraft - base de datos externa

import requests
import re


class Crawler():
    def __init__(self,tag):
        self.tag = tag
        self.url = 'https://www.shodan.io/search?query='
        self.servers = []
        self.ips = []

    def info(self):
        web = requests.get(self.url+self.tag)
        if web.status_code == 200:
             
            self.ips = re.findall(r'/host/(\d+\.\d+\.\d+\.\d+)',web.text)
                
            for ip in self.ips:
                yield ip
    

