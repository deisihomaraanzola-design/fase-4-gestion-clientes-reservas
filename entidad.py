
#importamos los elementos que necesitaremos para organizar las clases
from abc import ABC, abstractmethod

#Importamos la excepción personalizada para controlar los errores de los clientes
from excepciones_personalizadas import ErrorCliente

#Importamos la funcion que permite guardar los errores en el archivo de registro
from registro_logs import registrar_error


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
    #Creamos un método para consultar el identificador de la identidad
    def obtener_identificador(self):
        return self.__identificador
    #Creamos un método para consultar el nombre de la entidad
    def obtener_nombre(self):
        return self.__nombre

#Creamos la clase cliente para registrar los datos cada cliente
class Cliente(Entidad):

    #Creamos la clase para guardar los datos personales de los clientes
    def __init__(self, identificador, nombre, telefono, correo):
        super().__init__(identificador, nombre)
        self.__telefono = telefono
        self.__correo = correo

    #Creamos un método para validar los datos del cliente   
    def validar_datos(self):

        if not self.obtener_identificador():
            registrar_error("El identificador del cliente es necesario", "Cliente")
            raise ErrorCliente("El identificador del cliente es necesario")
        
        if not isinstance(self.obtener_nombre(), str) or not self.obtener_nombre().strip():
            registrar_error("El nombre del cliente es necesario", "Cliente")
            raise ErrorCliente("El nombre del cliente es necesario ")

        if not isinstance(self.__telefono, str) or not self.__telefono.strip():
            registrar_error("El telefono del cliente es necesario", "Cliente")
            raise ErrorCliente("El telefono del cliente es necesario")

        if not isinstance(self.__correo, str) or not self.__correo.strip():
            registrar_error("El correo del cliente es necesario", "Cliente")
            raise ErrorCliente("El correo del cliente es necesario")

        if "@" not in self.__correo:
            registrar_error("El correo electronico no es valido", "Cliente")
            raise ErrorCliente("El correo electronico no es valido")

        return True
    
    #Creamos un método para consultar el teléfono de el cliente 
    def obtener_telefono(self):
        return self.__telefono

    #Creamos un método para consultar el correo de el cliente
    def obtener_correo(self):
            return self.__correo

    
    
