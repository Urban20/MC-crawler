# modulo encargado de la UI del programa

from tkinter import  *
from servers import Buscar_Servers


titulo = 'MC Crawler'
dimension = "500x500"

class UI():
    def __init__(self,dimensiones :str ,titulo :str):
        self.dimension = dimensiones
        self.titulo = titulo
        self.pantalla = Tk()

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
    ui = UI(dimension,titulo)
    ui.crear_pantalla()
    ui.agregar_etiqueta("Rastrear servers",15)
    ui.crear_boton('Buscar servidores',Buscar_Servers)
    mainloop()