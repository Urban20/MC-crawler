'obtiene informacion de los servidores de minecraft edicion java'

import datetime
from mcstatus import JavaServer
from mcstatus.responses import JavaStatusResponse
from utilidades import consola
import clases.bot
import clases.MCuuid

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

        # informacion
        self.estado = 'offline'
        self.jugadores_online = ''
        self.motd = ''
        self.lista_jugadores = ''
        self.max_jugadores = None
        self.version = None
        self._p_onlines_raw = []
        self.p_data = []
        self.timeout = timeout
        self.info = None
        self.protocolo = 47
        self.ping = None # valor por default

        # caracteristicas del server
        self.withelist = False
        self.modeado = False
        self.veredicto = consola.ET_IND
        self.crackeado = False


    def __obtener_usuarios(self,estado : JavaStatusResponse):

        if estado.players.sample is not None:
            self._p_onlines_raw = estado.players.sample # tiene toda la info sin procesar

        for usuario in self._p_onlines_raw:
            
            self.p_data.append((usuario.name,usuario.id))
        

    def obtener_data(self,reintentos : int = 1):
        'metodo que actualiza la informacion de un servidor'
        for _ in range(reintentos):
            try:
                server = JavaServer.lookup(address=self.direccion,timeout=self.timeout)
                estado = server.status()
                self.version = estado.version.name.replace('\n',r'\n')
                self.max_jugadores = estado.players.max
                self.jugadores_online = estado.players.online
                self.motd = estado.motd.to_plain().replace('\n',r'\n').replace('\r', r'\r').strip()
                self.estado = 'online'
                self.__obtener_usuarios(estado)
                self.info = (self.direccion,self.pais,self.version,self.fecha)
                self.protocolo = estado.version.protocol
                self.ping = estado.latency 

                return self.estado            
            except TimeoutError:
                continue
            except :
                break
        
        return self.estado
        
    def verificar_crackeado(self):
        '''obtiene un verdedicto respecto a si el server es crackeado o no
        
        lo calcula en tiempo real'''
        if self.estado != 'online':
            return
        
        if self.p_data and clases.MCuuid.uuidV4(self.p_data[0][1]):
            
            # da una estimacion no tan precisa como a nivel de protocolo pero es mas rapida y
            # mejora la velocidad del programa para servidores puntuales
            
            self.veredicto = consola.ET_PREM
            return
        
        if self.p_data and clases.MCuuid.jugador_crackeado(usuario=self.p_data[0][0],
                                                           uuid=self.p_data[0][1]):
            # da una estimacion no tan precisa como a nivel de protocolo pero es mas rapida y
            # mejora la velocidad del programa para servidores puntuales
            
            self.veredicto = consola.ET_CRACK
            return

        clases.bot.desplegar_bot(self)

    def __pasear_info(self,**kwargs):
        t = ''
        for clave,valor in kwargs.items():
            t+= (' '*12) + f'{str(clave).replace('_',' ').capitalize()}: {str(valor)}\n\n'
        return t

                
    def print(self):


        titulo = f'IP : {self.direccion}'
    
        if self.estado == 'online':

            cuerpo = self.__pasear_info(
            veredicto=self.veredicto,
            ping=self.ping,
            whitelist_detectada=self.withelist,
            mods=self.modeado,
            fecha=self.fecha_otogada,
            nro_de_jugadores=f'{self.jugadores_online}/{self.max_jugadores}',
            version=self.version,
            motd=self.motd,
            jugadores_activos=self.p_data)

            consola.info_server(cuerpo=cuerpo, titulo=titulo)

        else:
            
            print(f'{self.direccion} - estado : {self.estado}')

        

    
        
