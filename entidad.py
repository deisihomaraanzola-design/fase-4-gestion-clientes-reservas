
# Importamos los elementos que necesitaremos para organizar las clases
from abc import ABC, abstractmethod

# Importamos la excepción personalizada para controlar los errores de los clientes
from excepciones_personalizadas import ErrorCliente

# Importamos las funciones para guardar errores y eventos en el registro
from registro_logs import registrar_error, registrar_evento


# Creamos la clase principal del sistema
class Entidad(ABC):

    # Creamos los datos que serviran para identificar cada elemento
    def __init__(self, identificador, nombre):
        self.__identificador = identificador
        self.__nombre = nombre

    # Creamos un metodo para validar los datos de las entidades
    @abstractmethod
    def validar_datos(self):
        pass

    # Creamos un metodo para consultar el identificador de la entidad
    def obtener_identificador(self):
        return self.__identificador

    # Creamos un metodo para consultar el nombre de la entidad
    def obtener_nombre(self):
        return self.__nombre


# Creamos la clase cliente para registrar los datos de cada cliente
class Cliente(Entidad):

    # Creamos el constructor para guardar los datos personales del cliente
    def __init__(self, identificador, nombre, telefono, correo):
        super().__init__(identificador, nombre)
        self.__telefono = telefono
        self.__correo = correo

    # Creamos un metodo para validar los datos del cliente
    def validar_datos(self):

        try:
            # Validamos el identificador del cliente
            if (
                not isinstance(self.obtener_identificador(), str)
                or not self.obtener_identificador().strip()
            ):
                raise ErrorCliente(
                    "El identificador del cliente es necesario y debe ser texto"
                )

            # Validamos el nombre del cliente
            if (
                not isinstance(self.obtener_nombre(), str)
                or not self.obtener_nombre().strip()
            ):
                raise ErrorCliente(
                    "El nombre del cliente es necesario"
                )

            # Validamos el telefono del cliente
            if (
                not isinstance(self.__telefono, str)
                or not self.__telefono.strip()
            ):
                raise ErrorCliente(
                    "El telefono del cliente es necesario"
                )

            # Validamos el correo electronico del cliente
            if (
                not isinstance(self.__correo, str)
                or not self.__correo.strip()
            ):
                raise ErrorCliente(
                    "El correo del cliente es necesario"
                )

            if "@" not in self.__correo:
                raise ErrorCliente(
                    "El correo electronico no es valido"
                )

        except ErrorCliente as error:
            registrar_error(error, "Cliente")
            raise

        except Exception as error:
            registrar_error(error, "Cliente")
            raise ErrorCliente(
                "Ocurrio un error inesperado al validar los datos del cliente"
            ) from error

        else:
            registrar_evento(
                "Los datos del cliente fueron validados correctamente",
                "Cliente"
            )
            return True

        finally:
            registrar_evento(
                "Finalizo el proceso de validacion del cliente",
                "Cliente"
            )

    # Creamos un metodo para consultar el telefono del cliente
    def obtener_telefono(self):
        return self.__telefono

    # Creamos un metodo para consultar el correo del cliente
    def obtener_correo(self):
        return self.__correo
