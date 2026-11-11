
#importamos los elementos que necesitaremos para organizar las clases
from abc import ABC, abstractmethod

#Creamos la clase principal del sistema 
class Entidad(ABC):

    #Creamos los datos que serviran para identificar cada elemento 
    def __init__(self, identificador, nombre):
        self.__identificador = identificador
        self.__nombre = nombre

    #Creamos un metodo para validar los datos de la entidades
    @abstractmethod
    def validar_datos(self):
        pass