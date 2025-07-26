# obtiene informacion de los servidores de minecraft edicion java
from mcstatus import JavaServer
import re

class McServer():
    def __init__(self,ip : str,puerto : int):
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
        self.timeout = 3

    def obtener_data(self):

        try:
            server = JavaServer.lookup(address=self.direccion,timeout=self.timeout)
            estado = server.status()

            self.version = estado.version.name
            self.max_jugadores = estado.players.max
            self.jugadores_online = estado.players.online
            self.motd = estado.motd.to_plain().strip()
            self.estado = 'online'
            self.p_onlines = re.findall(r"name='(\S+)'",str(estado.players.sample))
            
            self.info = None
            return self.estado
        
        except:

            return self.estado

    def __str__(self):
        
        if self.estado == 'online':

            self.info = f'ip: {self.direccion} | motd: {self.motd} | version: {self.version}\n'

            return f'''\n-----------------------------------------
            estado: {self.estado}

            ip: {self.direccion}

            motd : {self.motd}

            nro de jugadores : {self.jugadores_online}/{self.max_jugadores}

            version : {self.version}

            jugadores online: {self.p_onlines}
            \n-----------------------------------------
            '''
            
        else:
            
            return f'''
            {self.direccion} - estado : {self.estado}
            '''
        

    
        
