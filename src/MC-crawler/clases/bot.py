from mcproto.buffer import Buffer
from mcproto.connection import TCPSyncConnection
from mcproto.protocol.base_io import StructFormat
import clases.MCuuid
import re

# este bot se conecta a los servidores y determina por medio de la respuesta
# si se trata de un servidor no premium o premium, ademas se puede inferir si tiene mods o whitelist
# pero tiene un pequeño margen de error
# TENER EN CUENTA :
# - el bot no se refleja en el juego pero puede verse en la consola del servidor porque no completa el login
# - el bot no funciona en algunas versiones por cambios en el protocolo que son muy variados
# fallos encontrados en algunas versiones puntuales


def versionado_viejo(version : str): # EXPERIMENTAL
    reg = re.search(r'\d+\.\d+(?:\.\d)?',version)
    
    if not reg:
        return 
    
    return reg.group().split('.')[0] == '1'

def versionado_nuevo(version : str): # EXPERIMENTAL
    return versionado_viejo(version) == False # != None y != True

def protocolo_moderno(buffer : Buffer, version :str,uuid):
    '''
    aplica a versiones de la 1.20 +
    
    '''
    if re.search(r'1\.20(?:\.1)?$',version):
        # especificamente 1.20 / 1.20.1 -> EXCEPCION
        buffer.write_value(StructFormat.BOOL,False) 
        
        return

    
    # quitando la EXCEPCION : 1.20.2 +
    buffer.write(uuid.bytes)


def protocolo_antiguo(buffer : Buffer,version : str, nver : int):

    '''aplica a versiones 1.19 o anteriores'''

    if nver == 19: # se cubren excepciones
        rep = 2 if re.search(r'1\.19\.(?:1|2)$',version) else 1 # 1.19.1 / 1.19.2 -> EXCEPCION

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
        
        try:
            uuid = clases.MCuuid.uuid_Offline(self.usuario,string=False)
            buff = Buffer()
            buff.write_varint(self.paquete_inicial)
            buff.write_utf(self.usuario)

            if versionado_nuevo(version): # 26.1 y posteriores

                protocolo_moderno(buffer=buff,
                                  version=version,
                                  uuid=uuid)
                
            elif versionado_viejo(version): # formato 1.x.x o 1.x , ej 1.20, 1.19 , etc

                n_ver = int(re.search(r'1\.(\d+)(?:\.\d+)?',version).group(1))

                if n_ver in (20,21): # excepcion: 1.20.x - 1.21.x -> protocolo moderno
                    protocolo_moderno(buffer=buff,
                                  version=version,
                                  uuid=uuid)
                    
                else: # 1.19 y anteriores -> protocolo antiguo
                    protocolo_antiguo(buffer=buff,
                                    version=version,
                                    nver=n_ver)
                    
                
            self.__enviar_paquete(buff)
            
        except AttributeError: ...

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

