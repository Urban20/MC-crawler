# modulo encargado de la UI del programa

from tkinter import  *
from servers import Buscar_Servers,filtrar_info


titulo = 'MC Crawler'
dimension = "500x500"

class UI():
    'la clase UI es la encargada de manejar la interfaz grafica'
    def __init__(self,dimensiones :str ,titulo :str):
        self.dimension = dimensiones
        self.titulo = titulo
        self.pantalla = Tk()

    def crear_input(self):
        entrada = Entry(self.pantalla)
        entrada.pack()
        return entrada

    def agregar_etiqueta(self,texto : str,tamaño):
        et = Label(self.pantalla,text=texto,font=('Arial',tamaño))
        et.pack()
    
    def crear_boton(self,texto : str,funcion):
        boton = Button(self.pantalla,text=texto,command=funcion)
        boton.pack()

    def crear_pantalla(self):
        self.pantalla.title(self.titulo)
        self.pantalla.geometry(self.dimension)


def empaquetar():
    'esta funcion contiene TODOS los elementos de la interfaz grafica'
    ui = UI(dimension,titulo)
    ui.crear_pantalla()
    ui.agregar_etiqueta('Rastrear servers:',13)
    ui.crear_boton('Buscar servidores',Buscar_Servers)
    ui.agregar_etiqueta('buscar server por palabra clave: ',13)
    salida = ui.crear_input()
    ui.crear_boton('buscar',lambda : filtrar_info(salida.get()))
    mainloop()
    