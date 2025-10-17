'obtiene informacion de los servidores de minecraft edicion java'

import datetime
from mcstatus import JavaServer
import re
import MCuuid
import consola

class McServer():
    'esta clase es la encargada de obtener el estado y la informacion de los servidores'
    def __init__(self,ip : str,puerto=25565,fecha_otorgada = None,timeout = 1):
        self.fecha = datetime.datetime.today().isoformat(sep=' ',timespec='seconds')
        self.fecha_otogada = fecha_otorgada
        # fecha otorgada: es la fecha que se encuentra en la db para mostrar como info
        # no tiene relacion con self.fecha
        self.pais = '' # ya no se utiliza (obsoleto)
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
        self.timeout = timeout
        self.info = None
        self.veredicto = ''
        self.crackeado = 0 # inicialmente se toma el server como premium (0)
        # que self.crackeado sea crackeado = 1 no garantiza que realmente sea no premium pero da una estimacion
    def obtener_data(self,reintentos : int = 1):
        'metodo que actualiza la informacion de un servidor'
        for _ in range(reintentos):
            try:
                server = JavaServer.lookup(address=self.direccion,timeout=self.timeout)
                estado = server.status()
                self.version = estado.version.name
                self.max_jugadores = estado.players.max
                self.jugadores_online = estado.players.online
                self.motd = estado.motd.to_plain().replace('\n',' ').replace('\r', ' ').strip()
                self.estado = 'online'
                self.p_onlines = re.findall(r"name='(\S+)'",str(estado.players.sample)) # lista de jugadores online 
                self.uuid = re.findall(r"id='(\S+)'",str(estado.players.sample)) # lista de uuids
                self.p_data = list(zip(self.p_onlines,self.uuid)) # tupla (jugador, uuid)
                self.info = (self.direccion,self.pais,self.version,self.fecha)
                
                return self.estado
            except TimeoutError:
                continue
            except :
                break
        
        return self.estado
        
    def verificar_crackeado(self):
        '''obtiene un verdedicto respecto a si el server es crackeado o no
        
        lo calcula en tiempo real'''
        
        try:
            if self.p_data and self.estado == 'online':
                uuid_calculado = MCuuid.uuid_Offline(self.p_onlines[0])
                if uuid_calculado == self.uuid[0]:
                    self.crackeado = 1 


            if self.p_data and self.crackeado == 1:
                self.veredicto = '\033[0;32mposiblemente crackeado\033[0m'

            elif self.p_data and self.crackeado == 0 and re.search(r'\w+-\w+-4\w+-\w+-\w+',self.uuid[0]):
                self.veredicto = '\033[0;31mposiblemente premium\033[0m'
            
            else:
                self.veredicto = 'indeterminado'
   
        except AttributeError: ...

    def print(self):


        titulo = f'IP : {self.direccion}'
    
        if self.estado == 'online':

            cuerpo = f'''
            veredicto basado en jugador/es: {self.veredicto}

            registrado el dia: {self.fecha_otogada} 

            estado: {self.estado}

            motd: {self.motd}

            nro de jugadores: {self.jugadores_online}/{self.max_jugadores}

            version: {self.version}

            jugadores online: {self.p_data}
            
            '''

            consola.info_server(cuerpo=cuerpo, titulo=titulo)
        else:
            
            print(f'{self.direccion} - estado : {self.estado}')

        

    
        
