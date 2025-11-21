'obtiene informacion de los servidores de minecraft edicion java'

import datetime
from mcstatus import JavaServer
import re
from utilidades import consola
from clases.bot import Bot

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
        self.p_onlines = None
        self.timeout = timeout
        self.info = None
        self.protocolo = 47


        # etiquetas
        self.ET_CRACK = f'{consola.VERDE}crackeado/no premium{consola.RESET}'
        self.ET_PREM = f'{consola.ROJO}premium{consola.RESET}'
        self.ET_IND = f'indeterminado'
        self.ET_TIM = f'{consola.AMARILLO}tiempo agotado{consola.RESET}'
        self.ET_INC = f'{consola.CELESTE}protocolo incompatible{consola.RESET}'


        # caracteristicas del server
        self.withelist = False
        self.modeado = False
        self.veredicto = self.ET_IND
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
                self.protocolo = estado.version.protocol  

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
        try:
            
            bot = Bot(ip=self.ip,puerto=int(self.puerto),timeout=0.7)
            bot.conexion(num_proto=self.protocolo)
            bot.loguear(version=self.version)
            bot.leer_paquete()

            match bot.numero_estado:
    
                case 0: 

                    if re.search(r'whitelist|whitelisted|white-listed',
                                    bot.respuesta_str.lower()):
    
                        self.veredicto = self.ET_CRACK
                        self.crackeado = 1
                        self.withelist = True

                    elif re.search(r'mods|forge',bot.respuesta_str.lower()):

                        self.modeado = True
                    else:
                        self.veredicto = self.ET_INC
                        
                case 3:

                    self.veredicto = self.ET_CRACK
                    self.crackeado = 1

                case 1:

                    self.veredicto = self.ET_PREM

                case _:
                    self.veredicto = self.ET_IND
        except TimeoutError:
            self.veredicto = self.ET_TIM
        except:
            ...
                
    def print(self):


        titulo = f'IP : {self.direccion}'
    
        if self.estado == 'online':

            cuerpo = f'''
            veredicto: {self.veredicto}

            whitelist encontrada: {self.withelist}

            mods encontrados: {self.modeado}

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

        

    
        
