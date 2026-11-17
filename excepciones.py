
#Creamos la clase principal para identificar errores del sistema
class ErrorSistema(Exception):
    pass

#Creamos una excepcion para identificar y controlar los errores que se presenten al registrar los datos
class ErrorCliente(ErrorSistema):
    pass

#Creamos una excepción para manejar los errores de los servivios
class ErrorServicio(ErrorSistema):
    pass

#Creamos una excepción para identificar los errores en las reservas 
class ErrorReserva(ErrorSistema):
    pass

#Creamos una excepcion para identificar operaciones incorrectas durante la getión de reservas
class OperacionNoPermitida(ErrorReserva):
    pass

