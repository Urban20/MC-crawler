from mcproto.buffer import Buffer
from mcproto.connection import TCPSyncConnection
from mcproto.protocol.base_io import StructFormat
import MCuuid
import re

# este bot se conecta a los servidores y determina por medio de la respuesta
# si se trata de un servidor no premium o premium, ademas se puede inferir si tiene mods o whitelist
# pero tiene un pequeño margen de error
# TENER EN CUENTA :
# - el bot no se refleja en el juego pero puede verse en la consola del servidor porque no completa el login
# - el bot no funciona en algunas versiones por cambios en el protocolo que son muy variados
# fallos encontrados en algunas versiones puntuales de 1.19.x, 1.20.x



class Bot():
    'bot no premium para Minecraft java'
    def __init__(self,ip: str,puerto : int = 25565,usuario : str = 'McCrawler',timeout : int = 1):
        self.timeout = timeout
        self.usuario = usuario
        self.modo_login = 2
        self.paquete_inicial = 0
        self.ip = ip
        self.puerto = puerto
        self.__conex = ''
        self.respuerta = None # respuesta del server cuando responda
        self.respuesta_str = ''
        self.numero_estado = 0 # inicialmente aparece en 0 (no premium)
        self.conectado = False
  
    def conexion(self,num_proto : int = 47):
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

            self.__conex.write_varint(len(paquete))
            self.__conex.write(paquete)
            self.conectado = True
        except:
            print(f'[BOT] {self.usuario} >> no se pudo conectar a {self.ip}:{self.puerto}')

    def loguear(self,version : str = '1.21' ):
        
        if not self.conectado:
            return
        
        try:
            uuid = MCuuid.uuid_Offline(self.usuario,string=False)
            buff = Buffer()
            buff.write_varint(self.paquete_inicial)
            buff.write_utf(self.usuario)

            n_ver = int(re.search(r'1\.(\d+)(?:\.\d+)?',version).group(1))
            # se intenta cubrir la mayoria de los protocolos
            if n_ver == 20 or n_ver >= 21:
                buff.write(uuid.bytes)
            elif n_ver == 19:
                buff.write_value(StructFormat.BOOL,False)

            self.__conex.write_varint(len(buff))
            self.__conex.write(buff)
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

