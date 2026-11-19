
from abc import ABC, abstractmethod

#Importamos la excepción personalizada para controlar los errores de los servivios
from excepciones_personalizadas import ErrorServicio

#Importamos la funcion que permite guardar los errores y eventos en el archivo de registro.
from registro_logs import registrar_error, registrar_evento

# Clase abstracta que representa los servicios de Software FJ
class Servicio(ABC):

    def __init__(self, identificador, nombre, tarifa_base):
        self.__identificador = identificador
        self.__nombre = nombre
        self.__tarifa_base = tarifa_base

        self._validar_datos_generales()

    # Validamos los datos comunes de todos los servicios
    def _validar_datos_generales(self):

        if not isinstance(self.__identificador, str) or not self.__identificador.strip():
            registrar_error("El identificador del servicio es necesario.", "Servicio")
            raise ErrorServicio("El identificador del servicio es necesario.")

        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            registrar_error("El nombre del servicio es necesario.", "Servicio")
            raise ErrorServicio("El nombre del servicio es necesario.")

        if (
            isinstance(self.__tarifa_base, bool)
            or not isinstance(self.__tarifa_base, (int, float))
            or self.__tarifa_base <= 0
        ):
            registrar_error("La tarifa base debe ser un número mayor que cero.", "Servicio")
            raise ErrorServicio("La tarifa base debe ser un número mayor que cero.")

    # Métodos para consultar los atributos privados
    def obtener_identificador(self):
        return self.__identificador

    def obtener_nombre(self):
        return self.__nombre

    def obtener_tarifa_base(self):
        return self.__tarifa_base

    # Validamos los porcentajes de impuestos y descuentos
    def _validar_porcentajes(self, impuesto, descuento):

        for nombre, valor in [
            ("El impuesto", impuesto),
            ("El descuento", descuento)
        ]:
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or not 0 <= valor <= 100
            ):
                registrar_error(f"{nombre} debe estar entre 0 y 100.", "Servicio")
                raise ErrorServicio(
                    f"{nombre} debe estar entre 0 y 100."
                )

    # Métodos abstractos que deben implementar las clases hijas
    @abstractmethod
    def calcular_costo(self, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass


# Servicio especializado en reservas de salas
class ServicioSala(Servicio):

    def __init__(
        self, identificador, nombre, tarifa_base, capacidad, horas
    ):
        super().__init__(identificador, nombre, tarifa_base)
        self.__capacidad = capacidad
        self.__horas = horas

        self.validar_parametros()

    def validar_parametros(self):

        if (
            isinstance(self.__capacidad, bool)
            or not isinstance(self.__capacidad, int)
            or self.__capacidad <= 0
        ):
            registrar_error("La capacidad de la sala debe ser un entero mayor que cero.", "Servicio")
            raise ErrorServicio("La capacidad de la sala debe ser un entero mayor que cero.")

        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            registrar_error("Las horas de reserva deben ser mayores que cero.", "Servicio")
            raise ErrorServicio("Las horas de reserva deben ser mayores que cero.")

        return True

    def calcular_costo(self, impuesto=0, descuento=0):
        try:
            self.validar_parametros()
            self._validar_porcentajes(impuesto, descuento)

            subtotal = self.obtener_tarifa_base() * self.__horas
            total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        except ErrorServicio:
            raise

        except Exception as error:
            registrar_error(error, "Calculo del servicio de sala")
            raise ErrorServicio(
                "No fue posible calcular el costo del servicio de sala."
            ) from error

        else:
            registrar_evento(
                "Costo de sala calculado correctamente.",
                "Servicios"
            )
            return round(total, 2)

        finally:
            registrar_evento(
                "Finalizo el calculo del servicio de sala.",
                "Servicios"
            )

    def describir(self):
        return (
            f"Servicio de reserva de sala: {self.obtener_nombre()}. "
            f"Capacidad: {self.__capacidad} personas. "
            f"Duracion: {self.__horas} horas."
        )


# Servicio especializado en alquiler de equipos
class AlquilerEquipo(Servicio):

    def __init__(
        self, identificador, nombre, tarifa_base,
        equipo, cantidad, horas
    ):
        super().__init__(identificador, nombre, tarifa_base)
        self.__equipo = equipo
        self.__cantidad = cantidad
        self.__horas = horas

        self.validar_parametros()

    def validar_parametros(self):

        if not isinstance(self.__equipo, str) or not self.__equipo.strip():
            registrar_error("Debe especificar el nombre del equipo.", "Servicio")
            raise ErrorServicio("Debe especificar el nombre del equipo.")

        if (
            isinstance(self.__cantidad, bool)
            or not isinstance(self.__cantidad, int)
            or self.__cantidad <= 0
        ):
            registrar_error("La cantidad de equipos debe ser un entero mayor que cero.", "Servicio")
            raise ErrorServicio("La cantidad de equipos debe ser un entero mayor que cero.")

        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            registrar_error("Las horas de alquiler deben ser mayores que cero.", "Servicio")
            raise ErrorServicio("Las horas de alquiler deben ser mayores que cero.")

        return True

    def calcular_costo(self, impuesto=0, descuento=0):
        try:
            self.validar_parametros()
            self._validar_porcentajes(impuesto, descuento)

            subtotal = (
                self.obtener_tarifa_base()
                * self.__cantidad
                * self.__horas
            )

            total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        except ErrorServicio:
            raise

        except Exception as error:
            registrar_error(error, "Calculo del alquiler de equipos")
            raise ErrorServicio(
                "No fue posible calcular el costo del alquiler de equipos."
            ) from error

        else:
            registrar_evento(
                "Costo de alquiler de equipos calculado correctamente.",
                "Servicios"
            )
            return round(total, 2)

        finally:
            registrar_evento(
                "Finalizo el calculo del alquiler de equipos.",
                "Servicios"
            )

    def describir(self):
        return (
            f"Servicio de alquiler de equipos: {self.obtener_nombre()}. "
            f"Equipo: {self.__equipo}. "
            f"Cantidad: {self.__cantidad}. "
            f"Duracion: {self.__horas} horas."
        )


# Servicio especializado en asesorias
class AsesoriaEspecializada(Servicio):

    def __init__(
        self, identificador, nombre, tarifa_base,
        especialidad, horas
    ):
        super().__init__(identificador, nombre, tarifa_base)
        self.__especialidad = especialidad
        self.__horas = horas

        self.validar_parametros()

    def validar_parametros(self):

        if (
            not isinstance(self.__especialidad, str)
            or not self.__especialidad.strip()
        ):
            registrar_error("Debe especificar la especialidad.", "Servicio")
            raise ErrorServicio("Debe especificar la especialidad de la asesoria.")

        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            registrar_error("Las horas de asesoria deben ser mayores que cero.", "Servicio")
            raise ErrorServicio("Las horas de asesoria deben ser mayores que cero.")

        return True

    def calcular_costo(self, impuesto=0, descuento=0):
        try:
            self.validar_parametros()
            self._validar_porcentajes(impuesto, descuento)

            subtotal = self.obtener_tarifa_base() * self.__horas
            total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        except ErrorServicio:
            raise

        except Exception as error:
            registrar_error(error, "Calculo de asesoria especializada")
            raise ErrorServicio(
                "No fue posible calcular el costo de la asesoria especializada."
            ) from error

        else:
            registrar_evento(
                "Costo de asesoria especializada calculado correctamente.",
                "Servicios"
            )
            return round(total, 2)

        finally:
            registrar_evento(
                "Finalizo el calculo de la asesoria especializada.",
                "Servicios"
            )

    def describir(self):
        return (
            f"Servicio de asesoria especializada: {self.obtener_nombre()}. "
            f"Especialidad: {self.__especialidad}. "
            f"Duracion: {self.__horas} horas."
        )


# Prueba de funcionamiento de los servicios
if __name__ == "__main__":

    servicios = [
        ServicioSala("S001", "Sala de reuniones", 50000, 10, 2),
        AlquilerEquipo("E001", "Alquiler de equipos", 20000, "Proyector", 2, 3),
        AsesoriaEspecializada("A001", "Asesoria tecnologica", 80000, "Tecnologia", 2)
    ]

    print("SISTEMA DE SERVICIOS - SOFTWARE FJ")
    print("-----------------------------------")

    for servicio in servicios:
        print(servicio.describir())
        print(f"Costo sin ajustes: ${servicio.calcular_costo():,.2f}")
        print(
            f"Costo con impuesto del 19% y descuento del 10%: "
            f"${servicio.calcular_costo(19, 10):,.2f}"
        )
        print(f"Validacion: {servicio.validar_parametros()}")
        print("-----------------------------------")

    #Probamos el registro de errores al crear un servicio invalido.
    try:
        servicio_invalido = ServicioSala("", "Sala invalida", 50000, 10, 2)

    except ErrorServicio as error:
        registrar_error(error, "Prueba de servicio")
        print("\nError esperado en la prueba:", error)

    else:
        print("El servicio se creo correctamente")

    finally:
        print("La prueba de servicio ha finalizado")

    #Probamos el encadenamiento de excepciones en los servicios.
    servicio_prueba = ServicioSala("S002", "Sala de prueba", 50000, 10, 2)

    servicio_prueba.obtener_tarifa_base = lambda: 1 / 0

    try:
        servicio_prueba.calcular_costo()

    except ErrorServicio as error:
        registrar_error(error, "Prueba de encadenamiento")
        print("\nError generado:", type(error).__name__)
        print("Causa original:", type(error.__cause__).__name__)
