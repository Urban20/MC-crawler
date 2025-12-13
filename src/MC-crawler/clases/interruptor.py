import signal



class Interruptor():

    'maneja interrupciones de teclado (CTRL + C)'
    
    def __init__(self,evento : str):
        self.cancelado = False
        self.evento = evento
        
    def __manejador(self,num, f):

        print(f'\nel evento {self.evento} fue cancelado\n')
        self.cancelado = True

    def iniciar(self):
        print(f'\npulsar CTRL + C para cancelar el siguiente evento: {self.evento}\n')
        signal.signal(signal.SIGINT,self.__manejador)
    

