
from entidad import Cliente
from servicios import ServicioSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones_personalizadas import ErrorCliente, ErrorSistema, ErrorReserva, ErrorServicio
from registro_logs import registrar_error, registrar_evento

def probar_clientes():
    print("\n========== PRUEBAS DE CLIENTES ==========")

    #Operacion 1: registrar un cliente con datos validos.
    try:
        cliente1 = Cliente("C001", "Laura Gomez", "3001234567", "laura@gmail.com")
        cliente1.validar_datos()
        print("Operacion 1: Cliente registrado correctamente.")
        registrar_evento("Cliente C001 registrado correctamente.", "Clientes")

    except ErrorCliente as error:
        registrar_error(error, "Registro de cliente")
        print("Error al registrar el cliente:", error)

    #Operacion 2: intentar registrar un cliente con correo invalido.
    try:
        cliente2 = Cliente("C002", "Pedro Ruiz", "3101234567", "pedrogmail.com")
        cliente2.validar_datos()
        print("Operacion 2: Cliente registrado correctamente.")

    except ErrorCliente as error:
        registrar_error(error, "Registro de cliente invalido")
        print("Operacion 2: Error controlado:", error)

def probar_servicios():
    print("\n========== PRUEBAS DE SERVICIOS ==========")

    #Operacion 3: crear una sala correctamente.
    try:
        sala = ServicioSala("S003", "Sala de capacitacion", 60000, 15, 2)
        print("\nOperacion 3: Sala creada correctamente.")
        print("Costo:", sala.calcular_costo())
        registrar_evento("Sala S003 creada correctamente.", "Servicios")
    except ErrorServicio as error:
        registrar_error(error, "Prueba de sala")
        print("Error:", error)

    #Operacion 4: crear un alquiler de equipos.
    try:
        equipo = AlquilerEquipo("E002", "Alquiler de portatiles", 20000, "Portatil", 3, 2)
        print("\nOperacion 4: Alquiler creado correctamente.")
        print("Costo:", equipo.calcular_costo())
        registrar_evento("Alquiler E002 creado correctamente.", "Servicios")
    except ErrorServicio as error:
        registrar_error(error, "Prueba de alquiler")
        print("Error:", error)

    #Operacion 5: crear una asesoria especializada.
    try:
        asesoria = AsesoriaEspecializada("A002", "Asesoria de software", 80000, "Tecnologia", 2)
        print("\nOperacion 5: Asesoria creada correctamente.")
        print("Costo:", asesoria.calcular_costo())
        registrar_evento("Asesoria A002 creada correctamente.", "Servicios")
    except ErrorServicio as error:
        registrar_error(error, "Prueba de asesoria")
        print("Error:", error)

def probar_reservas():
    print("\n========== PRUEBAS DE RESERVAS ==========")

    cliente = Cliente(
    "C003", "Maria Lopez", "3001234568", "maria@gmail.com"
    )

    servicio = ServicioSala(
    "S004", "Sala de reuniones", 50000, 10, 2
    )

    #Operacion 6: crear y confirmar una reserva.
    try:
        reserva1 = Reserva(
            "R001", "Reserva de Maria", cliente, servicio, 2
        )
        reserva1.confirmar_reserva()
        print("\nOperacion 6: Reserva creada y confirmada.")
        registrar_evento("Reserva R001 confirmada.", "Reservas")

    except ErrorReserva as error:
        registrar_error(error, "Prueba de reserva")
        print("Error:", error)

    # Operacion 7: procesar una reserva confirmada.
    try:
        costo = reserva1.procesar_reserva()
        print("\nOperacion 7: Reserva procesada.")
        print("Costo:", costo)
        registrar_evento("Reserva R001 procesada.", "Reservas")

    except ErrorSistema as error:
        registrar_error(error, "Procesamiento de reserva")
        print("Error:", error)

    # Operacion 8: cancelar otra reserva.
    try:
        reserva2 = Reserva(
            "R002", "Reserva para cancelar", cliente, servicio, 2
        )
        reserva2.cancelar_reserva()
        print("\nOperacion 8: Reserva cancelada.")
        registrar_evento("Reserva R002 cancelada.", "Reservas")

    except ErrorSistema as error:
        registrar_error(error, "Cancelacion de reserva")
        print("Error:", error)

    # Operacion 9: intentar procesar una reserva pendiente.
    try:
        reserva3 = Reserva(
            "R003", "Reserva pendiente", cliente, servicio, 2
        )
        reserva3.procesar_reserva()

    except ErrorSistema as error:
        registrar_error(error, "Prueba de reserva pendiente")
        print("\nOperacion 9: Error controlado:", error)

    # Operacion 10: intentar crear una reserva sin identificador.
    try:
        reserva4 = Reserva(
            "", "Reserva invalida", cliente, servicio, 2
        )

    except ErrorSistema as error:
        registrar_error(error, "Prueba de reserva invalida")
        print("\nOperacion 10: Error controlado:", error)  

if __name__ == "__main__":
    probar_clientes()
    probar_servicios()
    probar_reservas()