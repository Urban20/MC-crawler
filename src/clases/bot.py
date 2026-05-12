from mcproto.buffer import Buffer
from mcproto.connection import TCPSyncConnection
from mcproto.protocol.base_io import StructFormat
import clases.MCuuid
import re
from utilidades import consola
from configuracion.configuracion import TIMEOUT_BOT

'''
 este bot se conecta a los servidores y determina por medio de la respuesta
 si se trata de un servidor no premium o premium, ademas se puede inferir si tiene mods o whitelist
 pero tiene un pequeño margen de error
 TENER EN CUENTA :
 - el bot no se refleja en el juego pero puede verse en la consola del servidor porque no completa el login
 - el bot no funciona en algunas versiones por cambios en el protocolo que son muy variados
 fallos encontrados en algunas versiones puntuales

'''

v20 = re.compile(r'1\.20(?:\.1)?$') # especificamente 1.20 / 1.20.1 -> EXCEPCION
v19 = re.compile(r'1\.19\.(?:1|2)$') # 1.19.1 / 1.19.2 -> EXCEPCION
versiones = re.compile(r'\d+\.\d+(?:\.\d)?')
ver_vieja = re.compile(r'1\.(\d+)(?:\.\d+)?')



def n_ver(version : str):
    '''

    NUMERO DE VERSION:

    extrae la numerologia del medio para las versiones
    
    solo tiene sentido en el versionado antiguo (26.0 + no tiene sentido real)

    ejemplo: 

    - 1.20.1 -> retorna 20
    
    - 1.8.x-1.21.x -> retorna el primer numero del bloque de versiones : 8 

    - version invalida -> retorna None
    
    
    '''
    r = ver_vieja.search(version)

    if r is None or versionado_nuevo(version):
        return
    
    return int(r.group(1))
    

def versionado_viejo(version : str):
    '''
    posibles retornos:

    1) True -> si coincide con versionado viejo

    2) None -> si la notacion es invalida

    3) False -> si la notacion es correcta pero no pertenece a versionados viejos
    
    '''


    reg = versiones.search(version)
    
    if not reg or len(version.split('.')) not in (2,3):
        return 
    
    return reg.group().split('.')[0] == '1'

def versionado_nuevo(version : str):

    '''
    1) True -> corresponde a versiones nuevas

    2) False -> no corresponde
    
    '''

    return versionado_viejo(version) is False # != None y != True

def protocolo_moderno(buffer : Buffer, version :str,uuid):
    '''
    aplica a versiones de la 1.20 +
    
    '''
    if v20.search(version):
        
        buffer.write_value(StructFormat.BOOL,False) 
        
        return

    
    # quitando la EXCEPCION : 1.20.2 +
    buffer.write(uuid.bytes)


def protocolo_antiguo(buffer : Buffer,version : str, nver : int):

    '''aplica a versiones 1.19 o anteriores'''

    if nver == 19: # se cubren excepciones
        rep = 2 if v19.search(version) else 1 # 1.19.1 / 1.19.2 -> EXCEPCION

        for _ in range(rep):
            buffer.write_value(StructFormat.BOOL,False)
    

class Bot():
    'bot no premium para Minecraft java'
    def __init__(self,ip: str,puerto : int = 25565,usuario : str = 'ObserverBOT',timeout : int = 1):
        self.timeout = timeout
        self.usuario = usuario
        self.modo_login = 2
        self.paquete_inicial = 0
        self.ip = ip
        self.puerto = puerto
        self.__conex = ''
        self.respuerta = None # respuesta del server cuando responda
        self.respuesta_str = ''
        self.numero_estado = 0
        self.conectado = False

        self.pid_desconexion = 0
        self.pid_encript = 1
        self.pid_login = 3
    
    def __enviar_paquete(self,buffer : Buffer):
        self.__conex.write_varint(len(buffer))
        self.__conex.write(buffer)
  
    def conexion(self,num_proto : int = 47): # handshake
        try:
            self.__conex = TCPSyncConnection.make_client((self.ip,self.puerto),self.timeout)
            hand = Buffer()
            hand.write_varint(num_proto)
            hand.write_utf(self.ip)
            hand.write_value(StructFormat.USHORT,self.puerto)
            hand.write_varint(self.modo_login)


            paquete = Buffer()
            paquete.write_varint(self.paquete_inicial)
            paquete.write(hand)

            self.__enviar_paquete(paquete)
            
            self.conectado = True
        except:
            print(f'[BOT] {self.usuario} >> no se pudo conectar a {self.ip}:{self.puerto}')

    def loguear(self,version : str = '1.21' ):
        
        if not self.conectado:
            return
        
        
        uuid = clases.MCuuid.uuid_Offline(self.usuario,string=False)
        buff = Buffer()
        buff.write_varint(self.paquete_inicial)
        buff.write_utf(self.usuario)

        if versionado_nuevo(version): # 26.1 y posteriores

            protocolo_moderno(buffer=buff,
                                version=version,
                                uuid=uuid)
            
        elif versionado_viejo(version): # formato 1.x.x o 1.x , ej 1.20, 1.19 , etc

            num = n_ver(version)

            if num in (20,21): # excepcion: 1.20.x - 1.21.x -> protocolo moderno
                protocolo_moderno(buffer=buff,
                                version=version,
                                uuid=uuid)
                
            else: # 1.19 y anteriores -> protocolo antiguo
                protocolo_antiguo(buffer=buff,
                                version=version,
                                nver=num)
                
            
        self.__enviar_paquete(buff)
            
        

    def leer_paquete(self):

        if not self.conectado:
            return
        
        varint = self.__conex.read_varint()
        n_resp = self.__conex.read(varint)
        self.respuerta = n_resp
        self.respuesta_str = n_resp.decode(errors='replace')
        buffer = Buffer(n_resp).read_varint()
        self.numero_estado = buffer
        self.__conex.close()

def desplegar_bot(server):

    try:
            
        bot = Bot(ip=server.ip,puerto=int(server.puerto),timeout=TIMEOUT_BOT)
        bot.conexion(num_proto=server.protocolo)
        bot.loguear(version=server.version)
        bot.leer_paquete()

    except TimeoutError:
        server.veredicto = consola.ET_TIM
        return
    except:
        server.veredicto = consola.ET_INC
        return
    
    obtener_veredicto(bot,server)


def obtener_veredicto(bot : Bot, server):

    '''
    funcion auxiliar de desplegar_bot( )

    esta funcion decide como se clasifica el veredicto para c/servidor
    
    '''

    match bot.numero_estado:
            
        case bot.pid_desconexion: 
            
            paquete_disconnect(server,bot)
                
        case bot.pid_login:

            server.veredicto = consola.ET_CRACK
            server.crackeado = True

        case bot.pid_encript:

            server.veredicto = consola.ET_PREM

        case _:
            server.veredicto = consola.ET_IND


def paquete_disconnect(server,bot):

    '''
    funcion auxiliar de obtener_veredicto( )

    maneja la logica en caso de pid = 0 (disconnect)
    
    '''
    coincidencia = lambda reg: re.search(reg,bot.respuesta_str.lower())

    if coincidencia(r'whitelist|whitelisted|white-listed'):

        server.veredicto = consola.ET_CRACK
        server.crackeado = True
        server.withelist = True

    elif coincidencia(r'mods|forge'):

        server.veredicto = consola.ET_MOD
        server.modeado = True

    elif coincidencia(r'banned'):

        server.veredicto = consola.ET_BAN

    else:
        server.veredicto = consola.ET_IND