
#Utilizamos la herramienta logging para almacenar información sobre los errores
#que se presenten en el programa al registrar clientes,gestionar servicios o realizar reservas.
import logging

#Configuramos el registro para guardar los errores en un archivo llamado 
#errores.log,incluimos la fecha, hora y mensaje de error.
logging.basicConfig(
    force=True,
    filename="errores.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def registrar_error(error, modulo="Sistema"):
    #Creamos una función para guardar los errores que ocurran en el sistema
    logging.error(f"{modulo}: {error}")

#Registramos los eventos importantes que ocurren en el sistema.
def registrar_evento(mensaje, modulo="Sistema"):
    logging.info(f"{modulo}: {mensaje}")