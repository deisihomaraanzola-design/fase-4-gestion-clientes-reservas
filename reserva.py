
from entidad import Entidad
from entidad import Cliente
from servicios import ServicioSala
from excepciones_personalizadas import ErrorSistema, ErrorReserva, OperacionNoPermitida

# Creamos la clase Reserva para administrar las reservas de los clientes
class Reserva(Entidad):

    # Creamos el constructor para guardar los datos de cada reserva
    def __init__(self, identificador, nombre, cliente, servicio, duracion):
        super().__init__(identificador, nombre)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

        self.validar_datos()

    # Creamos un metodo para validar los datos de la reserva
    def validar_datos(self):

        if not isinstance(self.obtener_identificador(), str) or not self.obtener_identificador().strip():
            raise ErrorReserva("El identificador de la reserva es necesario")

        if not isinstance(self.obtener_nombre(), str) or not self.obtener_nombre().strip():
            raise ErrorReserva("El nombre de la reserva es necesario")

        if not isinstance(self.__cliente, Entidad):
            raise ErrorReserva("Debe registrar un cliente valido")

        if not callable(getattr(self.__cliente, "validar_datos", None)):
            raise ErrorReserva("El cliente no tiene un metodo de validacion")

        if not callable(getattr(self.__servicio, "validar_parametros", None)):
            raise ErrorReserva("Debe seleccionar un servicio valido")

        if not callable(getattr(self.__servicio, "calcular_costo", None)):
            raise ErrorReserva("El servicio no permite calcular su costo")

        if (
            isinstance(self.__duracion, bool)
            or not isinstance(self.__duracion, (int, float))
            or self.__duracion <= 0
        ):
            raise ErrorReserva("La duracion de la reserva debe ser mayor que cero")

        self.__cliente.validar_datos()
        self.__servicio.validar_parametros()

        return True

    # Creamos un metodo para confirmar la reserva
    def confirmar_reserva(self):

        if self.__estado != "Pendiente":
            raise ErrorReserva("Solo se pueden confirmar reservas pendientes")

        self.validar_datos()
        self.__estado = "Confirmada"

        return True

    # Creamos un metodo para cancelar la reserva
    def cancelar_reserva(self):

        if self.__estado == "Cancelada":
            raise ErrorReserva("La reserva ya se encuentra cancelada")

        if self.__estado == "Procesada":
            raise ErrorReserva("No se puede cancelar una reserva procesada")

        self.__estado = "Cancelada"

        return True

    # Creamos un metodo para procesar la reserva
    def procesar_reserva(self):

        if self.__estado != "Confirmada":
            raise ErrorReserva("La reserva debe estar confirmada para procesarse")

        self.validar_datos()

        costo = self.__servicio.calcular_costo()
        self.__estado = "Procesada"

        return costo

    # Creamos un metodo para consultar el estado de la reserva
    def obtener_estado(self):
        return self.__estado

    # Creamos un metodo para consultar el cliente de la reserva
    def obtener_cliente(self):
        return self.__cliente

    # Creamos un metodo para consultar el servicio de la reserva
    def obtener_servicio(self):
        return self.__servicio

    # Creamos un metodo para consultar la duracion de la reserva
    def obtener_duracion(self):
        return self.__duracion

    # Creamos un metodo para describir la reserva
    def describir(self):

        return (
            f"Reserva: {self.obtener_nombre()}. "
            f"Cliente: {self.__cliente.obtener_nombre()}. "
            f"Servicio: {self.__servicio.obtener_nombre()}. "
            f"Duracion: {self.__duracion} horas. "
            f"Estado: {self.__estado}."
        )


# Pruebas de funcionamiento de la clase Reserva
if __name__ == "__main__":

    try:
        cliente = Cliente(
            "C001",
            "Carlos Perez",
            "3001234567",
            "carlos@gmail.com"
        )

        servicio = ServicioSala(
            "S001",
            "Sala de reuniones",
            50000,
            10,
            2
        )

        reserva = Reserva(
            "R001",
            "Reserva de sala",
            cliente,
            servicio,
            2
        )

        print("\nSISTEMA DE RESERVAS - SOFTWARE FJ")
        print("-----------------------------------")

        print("\nReserva creada:")
        print(reserva.describir())

        reserva.confirmar_reserva()
        print("\nReserva confirmada:")
        print("Estado:", reserva.obtener_estado())

        costo = reserva.procesar_reserva()
        print("\nReserva procesada:")
        print("Costo:", costo)
        print("Estado:", reserva.obtener_estado())

        reserva_cancelada = Reserva(
            "R002",
            "Reserva para cancelar",
            cliente,
            servicio,
            2
        )

        reserva_cancelada.cancelar_reserva()
        print("\nPrueba de cancelacion:")
        print(reserva_cancelada.describir())

    except ErrorSistema as error:
        print("\nError en la reserva:", error)

