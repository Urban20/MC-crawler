from mcproto.buffer import Buffer
from mcproto.connection import TCPSyncConnection
from mcproto.protocol.base_io import StructFormat
import MCuuid

# este bot se conecta a los servidores y determina por medio de la respuesta
# si se trata de un servidor no premium o premium
# TENER EN CUENTA : el bot no se refleja en el juego pero puede verse en la consola
# del servidor
# autor : Urban - Matias Urbaneja

class Bot():
    'bot no premium para Minecraft java'
    def __init__(self,ip: str,puerto : int = 25565,usuario = 'McCrawler',timeout : int = 1):
        self.timeout = timeout
        self.usuario = usuario
        self.modo_login = 2
        self.paquete_inicial = 0
        self.ip = ip
        self.puerto = puerto
        self.__conex = ''
        self.respuerta = None # respuesta del server cuando responda
        self.respuesta_str = None 
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
            print(f'{self.usuario} >> no se pudo conecta a {self.ip}')

    def loguear(self):
        if self.conectado:
            uuid = MCuuid.uuid_Offline(self.usuario,string=False)
            buff = Buffer()
            buff.write_varint(self.paquete_inicial)
            buff.write_utf(self.usuario)
            buff.write(uuid.bytes)

            self.__conex.write_varint(len(buff))
            self.__conex.write(buff)

    def leer_paquete(self):
        if self.conectado:
            varint = self.__conex.read_varint()
            n_resp = self.__conex.read(varint)
            self.respuerta = n_resp
            self.respuesta_str = str(n_resp)
            buffer = Buffer(n_resp).read_varint()
            self.numero_estado = buffer

