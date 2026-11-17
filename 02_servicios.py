
from abc import ABC, abstractmethod


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
            raise ValueError("El identificador del servicio es necesario.")

        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            raise ValueError("El nombre del servicio es necesario.")

        if (
            isinstance(self.__tarifa_base, bool)
            or not isinstance(self.__tarifa_base, (int, float))
            or self.__tarifa_base <= 0
        ):
            raise ValueError("La tarifa base debe ser un número mayor que cero.")

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
                raise ValueError(
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
            raise ValueError("La capacidad de la sala debe ser un entero mayor que cero.")

        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            raise ValueError("Las horas de reserva deben ser mayores que cero.")

        return True

    def calcular_costo(self, impuesto=0, descuento=0):
        self.validar_parametros()
        self._validar_porcentajes(impuesto, descuento)

        subtotal = self.obtener_tarifa_base() * self.__horas
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        return round(total, 2)

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
            raise ValueError("Debe especificar el nombre del equipo.")

        if (
            isinstance(self.__cantidad, bool)
            or not isinstance(self.__cantidad, int)
            or self.__cantidad <= 0
        ):
            raise ValueError("La cantidad de equipos debe ser un entero mayor que cero.")

        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            raise ValueError("Las horas de alquiler deben ser mayores que cero.")

        return True

    def calcular_costo(self, impuesto=0, descuento=0):
        self.validar_parametros()
        self._validar_porcentajes(impuesto, descuento)

        subtotal = (
            self.obtener_tarifa_base()
            * self.__cantidad
            * self.__horas
        )

        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        return round(total, 2)

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
            raise ValueError("Debe especificar la especialidad de la asesoria.")

        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            raise ValueError("Las horas de asesoria deben ser mayores que cero.")

        return True

    def calcular_costo(self, impuesto=0, descuento=0):
        self.validar_parametros()
        self._validar_porcentajes(impuesto, descuento)

        subtotal = self.obtener_tarifa_base() * self.__horas
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        return round(total, 2)

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
