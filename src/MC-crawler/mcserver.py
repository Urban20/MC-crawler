'obtiene informacion de los servidores de minecraft edicion java'

import datetime
from mcstatus import JavaServer
import re

class McServer():
    'esta clase es la encargada de obtener el estado y la informacion de los servidores'
    def __init__(self,ip : str,puerto=25565,pais='desconocido',fecha_otorgada = None):
        self.fecha = datetime.datetime.today().isoformat(sep=' ',timespec='seconds')
        self.fecha_otogada = fecha_otorgada
        # fecha otorgada: es la fecha que se encuentra en la db para mostrar como info
        # no tiene relacion con self.fecha
        self.pais = pais
        self.ip = ip
        self.puerto = puerto
        self.direccion = self.ip + ':' + str(self.puerto)
        self.estado = 'offline'
        self.jugadores_online = ''
        self.motd = ''
        self.lista_jugadores = ''
        self.max_jugadores = None
        self.version = None
        self.p_onlines = None
        self.timeout = 1
        self.info = None
    def obtener_data(self):
        'metodo que actualiza la informacion de un servidor'
        try:
            server = JavaServer.lookup(address=self.direccion,timeout=self.timeout)
            estado = server.status()

            self.version = estado.version.name
            self.max_jugadores = estado.players.max
            self.jugadores_online = estado.players.online
            self.motd = estado.motd.to_plain().replace('\n',' ').replace('\r', ' ').strip()
            self.estado = 'online'
            self.p_onlines = re.findall(r"name='(\S+)'",str(estado.players.sample))
            self.uuid = re.findall(r"id='(\S+)'",str(estado.players.sample))
            self.p_data = list(zip(self.p_onlines,self.uuid))
            self.info = (self.direccion,self.pais,self.version,self.fecha)
            
            return self.estado
        
        except:

            return self.estado

    def __str__(self):
        
        if self.estado == 'online':

            return f'''\n-----------------------------------------
            registrado el dia : {self.fecha_otogada} 

            estado: {self.estado}

            ip: {self.direccion}

            pais: {self.pais}

            motd: {self.motd}

            nro de jugadores: {self.jugadores_online}/{self.max_jugadores}

            version: {self.version}

            jugadores online: {self.p_data}
            \n-----------------------------------------
            '''
            
        else:
            
            return f'''
            {self.direccion} - estado : {self.estado}
            '''
        

    
        
