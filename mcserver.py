# obtiene informacion de los servidores de minecraft edicion java
from mcstatus import JavaServer



class McServer():
    def __init__(self,direccion : str):
        self.direccion = direccion
        self.estado = 'offline'
        self.jugadores_online = ''
        self.motd = ''
        self.lista_jugadores = ''
        self.max_jugadores = None
        self.version = None

    def obtener_data(self):

        try:
            server = JavaServer.lookup(address=self.direccion,timeout=3)
            estado = server.status()

            self.version = estado.version.name
            self.max_jugadores = estado.players.max
            self.jugadores_online = estado.players.online
            self.motd = estado.motd.to_plain().strip()
            self.estado = 'online'
            
            return self.estado
        
        except Exception as e:

            return self.estado

    def __str__(self):
        
        if self.estado == 'online':
            return f'''
            estado: {self.estado}

            ip: {self.direccion}

            motd : {self.motd}

            nro de jugadores : {self.jugadores_online}/{self.max_jugadores}

            version : {self.version}
            '''
        else:
            
            return f'''
            {self.direccion} - estado : {self.estado}
            '''
        

    
        
