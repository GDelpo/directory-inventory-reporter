from datetime import datetime
import win32security
from pathlib import Path

from logger import error_logger

def obtener_propietario_archivo(nombre_archivo):
    """
    Obtiene el propietario de un archivo en Windows.

    Args:
        nombre_archivo (Path obj): El nombre o la ruta del archivo.
    Returns: 
        str: El nombre del propietario del archivo o una cadena vacía si no se puede determinar.
    """
    propietario = ""
    try:
        nombre_archivo = nombre_archivo.resolve()  # Resuelve rutas absolutas y simbólicas.
        # Obtener la información de seguridad del archivo, incluyendo el propietario.
        sd = win32security.GetFileSecurity(str(nombre_archivo), win32security.OWNER_SECURITY_INFORMATION)
        
        # Obtener el SID del propietario.
        sid_propietario = sd.GetSecurityDescriptorOwner()
        
        # Obtener la cuenta del propietario en formato (nombre, dominio, tipo).
        cuenta_propietario = win32security.LookupAccountSid(None, sid_propietario)
        
        # Obtener el nombre del propietario.
        propietario = cuenta_propietario[0]
    except FileNotFoundError as e:
        # Registra el error en lugar de imprimirlo directamente
        error_logger.error(f"El archivo no se encontró: {nombre_archivo}")
    except PermissionError as e:
        # Registra el error en lugar de imprimirlo directamente
        error_logger.error(f"No tiene permiso para acceder al archivo: {nombre_archivo}")
    except Exception as e:
        # Registra el error en lugar de imprimirlo directamente
        error_logger.error(f"Error al obtener el propietario del archivo {nombre_archivo}: {e}")
    return propietario

    
def obtener_fecha_modificacion_archivo_o_directorio(ruta_archivo_o_directorio):
    """
    Obtiene la fecha de modificación de un archivo o directorio en un formato legible.

    Args:
        ruta_archivo_o_directorio (str): La ruta al archivo o directorio del cual se quiere obtener la fecha de modificación.

    Returns:
        str: La fecha de modificación en formato 'dd-mm-YYYY' o None si ocurre un error.
    """
    fecha_modificacion = None
    try:
        ruta_archivo_o_directorio = Path(ruta_archivo_o_directorio).resolve()  # Resuelve rutas absolutas y simbólicas.
        if ruta_archivo_o_directorio.exists():
            # Obtener la fecha de modificación en un formato legible
            info_estado = ruta_archivo_o_directorio.lstat()
            fecha_modificacion = datetime.fromtimestamp(info_estado.st_mtime)
    except FileNotFoundError as e:
        # Registra el error en lugar de imprimirlo directamente
        error_logger.error(f"El archivo o directorio no se encontró: {ruta_archivo_o_directorio}")
    except PermissionError as e:
        # Registra el error en lugar de imprimirlo directamente
        error_logger.error(f"No tiene permiso para acceder al archivo o directorio: {ruta_archivo_o_directorio}")
    except Exception as e:
        # Registra el error en lugar de imprimirlo directamente
        error_logger.error(f"Error al obtener la fecha de modificación del archivo o directorio {ruta_archivo_o_directorio}: {e}")
    return fecha_modificacion

def obtener_info_archivo(elemento):
    tipo_archivo = 'Es una carpeta' if elemento.is_dir() else elemento.suffix
    return {
        "nombre": elemento.name,
        "fecha_modificacion": obtener_fecha_modificacion_archivo_o_directorio(elemento),
        "propietario": obtener_propietario_archivo(elemento),
        "tipo_archivo": tipo_archivo,
        "peso_en_mbs": 0 if elemento.is_dir() else float(elemento.stat().st_size / 1024 / 1024) # Peso en MB
    }

def obtener_listado_archivos(directorio_padre):
    """
    Obtiene información sobre los archivos en un directorio.

    Args:
        directorio_padre (str): Ruta del directorio que deseas listar.

    Returns:
        list: Una lista de diccionarios con información de los archivos.
    """
    directorio_a_recorrer = Path(directorio_padre)
    info_directorio = []

    try:
        # Comprobar si la ruta es un directorio
        if directorio_a_recorrer.is_dir():
            for elemento in directorio_a_recorrer.iterdir():
                info_directorio.append(obtener_info_archivo(elemento))
        else:
            error_logger.error("La ruta no es un directorio.")
    except OSError as e:
        error_logger.error(f"Error al acceder al directorio: {str(e)}")

    return info_directorio