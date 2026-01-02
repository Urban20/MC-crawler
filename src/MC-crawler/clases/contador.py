class Contador_busqueda_servers():
    '''contador invocado al hacer barridos de bloques
    
    - evita el uso de variables globales'''

    def __init__(self):
        self.encontrados = 0
        self.actualizado = 0
    
    def incrementar_encontrados(self):
        self.encontrados += 1
    def incrementar_actualizados(self):
        self.actualizado += 1
 
    def resetear(self):
        self.encontrados = 0
        self.actualizado = 0
       

contador = Contador_busqueda_servers()