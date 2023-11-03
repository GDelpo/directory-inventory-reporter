import time
import logging
import win32security
from pathlib import Path
import pandas as pd

# Configura la configuración de registro, como el nombre del archivo y el nivel de registro
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


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
        logging.error(f"El archivo no se encontró: {nombre_archivo}")
    except PermissionError as e:
        # Registra el error en lugar de imprimirlo directamente
        logging.error(f"No tiene permiso para acceder al archivo: {nombre_archivo}")
    except Exception as e:
        # Registra el error en lugar de imprimirlo directamente
        logging.error(f"Error al obtener el propietario del archivo {nombre_archivo}: {e}")
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
            fecha_modificacion = time.strftime('%d-%m-%Y', time.localtime(info_estado.st_mtime))
    except FileNotFoundError as e:
        # Registra el error en lugar de imprimirlo directamente
        logging.error(f"El archivo o directorio no se encontró: {ruta_archivo_o_directorio}")
    except PermissionError as e:
        # Registra el error en lugar de imprimirlo directamente
        logging.error(f"No tiene permiso para acceder al archivo o directorio: {ruta_archivo_o_directorio}")
    except Exception as e:
        # Registra el error en lugar de imprimirlo directamente
        logging.error(f"Error al obtener la fecha de modificación del archivo o directorio {ruta_archivo_o_directorio}: {e}")
    return fecha_modificacion

def obtener_info_archivo(elemento):
    tipo_archivo = 'Es una carpeta' if elemento.is_dir() else elemento.suffix
    return {
        "nombre": elemento.name,
        "fecha_modificacion": obtener_fecha_modificacion_archivo_o_directorio(elemento),
        "propietario": obtener_propietario_archivo(elemento),
        "tipo_archivo": tipo_archivo
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
            logging.error("La ruta no es un directorio.")
    except OSError as e:
        logging.error(f"Error al acceder al directorio: {str(e)}")

    return info_directorio

def dividir_df_por_propietario(dataframe):
    """
    Divide un DataFrame en varios DataFrames, uno por cada propietario, organizándolos por tipo de archivo y fecha.

    Args:
        dataframe (pd.DataFrame): El DataFrame que contiene información de archivos con propietario.

    Returns:
        dict: Un diccionario donde las claves son los nombres de los propietarios y los valores son DataFrames que contienen sus archivos.
    """
    # Filtrar los archivos sin propietario definido
    sin_propietario = dataframe[dataframe['propietario'].isna() | (dataframe['propietario'] == '')]

    # Filtrar los archivos con propietario definido
    con_propietario = dataframe[dataframe['propietario'].notna() & (dataframe['propietario'] != '')]

    # Crear un diccionario de DataFrames, uno por cada propietario
    diccionario_por_propietario = {}

    # Organiza por tipo de archivo y luego por fecha
    con_propietario = con_propietario.sort_values(by=['propietario', 'tipo_archivo', 'fecha_modificacion'])

    # Usa groupby para dividir el DataFrame por propietario
    for propietario, grupo in con_propietario.groupby('propietario'):
        diccionario_por_propietario[propietario] = grupo.copy()

    diccionario_por_propietario['totalizador'] = obtener_totalizador(diccionario_por_propietario)
    diccionario_por_propietario['sin propietario'] = sin_propietario

    return diccionario_por_propietario

def obtener_totalizador(diccionario_por_propietario):
    """
    Obtiene un DataFrame que contiene el totalizador de registros por propietario.

    Args:
        diccionario_por_propietario (dict): Un diccionario con DataFrames organizados por propietario.

    Returns:
        pd.DataFrame: Un DataFrame que contiene el totalizador de registros por propietario.
    """
    lista_totalizador = []
    
    for propietario, dataframe in diccionario_por_propietario.items():
        if propietario not in ('totalizador', 'sin propietario'):
            num_filas = len(dataframe)
            lista_totalizador.append((propietario, num_filas))
    
    totalizador_df = pd.DataFrame(lista_totalizador, columns=['Propietario', 'Cantidad de registros en total'])
    totalizador_df = totalizador_df.sort_values(by='Propietario')
    
    return totalizador_df

def ordenar_claves(diccionario):
    """
    Ordena las claves de un diccionario de manera específica, colocando 'totalizador' y 'sin propietario' al principio.
    
    Args:
        diccionario (dict): El diccionario cuyas claves se van a ordenar.
     
    Returns:
        list: Lista de claves ordenadas.
    """
    
    # Obtiene todas las claves, excluyendo 'totalizador' y 'sin propietario'
    claves_excluidas = ('totalizador', 'sin propietario')
    claves_ordenar = [clave for clave in diccionario.keys() if clave not in claves_excluidas]

    # Ordena las claves alfabéticamente
    claves_ordenadas = sorted(claves_ordenar)

    # Agrega 'totalizador' y 'sin propietario' al comienzo de la lista de claves ordenadas
    claves_ordenadas = ['totalizador', 'sin propietario'] + claves_ordenadas

    return claves_ordenadas

def exportar_diccionario_a_excel(diccionario, orden_claves, nombre_archivo='informe_directorio.xlsx'):
    """
    Exporta un diccionario de DataFrames a un archivo de Excel con hojas ordenadas según una lista de claves.

    Args:
        diccionario (dict): Un diccionario que contiene DataFrames asociados a propietarios.
        orden_claves (list): Una lista de claves que determina el orden de las hojas en el archivo de Excel.
        nombre_archivo (str): El nombre del archivo de Excel de destino. (por defecto, 'archivo_excel.xlsx')
    """
    # Crear un nuevo libro de Excel
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as escritor_excel:
        for clave in orden_claves:
            # Obtener el DataFrame para este propietario
            dataframe = diccionario[clave]

            # Reemplazar los espacios en blanco en los nombres de las hojas por guiones bajos
            nombre_hoja = clave.replace(' ', '_')

            # Escribir el DataFrame en la hoja correspondiente
            dataframe.to_excel(escritor_excel, sheet_name=nombre_hoja, index=False)

def generar_reporte_directorio(ruta_seleccionada):

    # Obtener una lista de archivos de la ruta 
    lista_archivos = obtener_listado_archivos(ruta_seleccionada)

    # Crear un DataFrame a partir de la lista de diccionarios
    df = pd.DataFrame(lista_archivos)

    # Dividir el DataFrame por propietario
    diccionario_por_propietario = dividir_df_por_propietario(df)

    # Obtener las claves ordenadas del diccionario
    claves_ordenadas = ordenar_claves(diccionario_por_propietario)

    # Llamar al método exportar_diccionario_a_excel pasando el diccionario, las claves ordenadas y el nombre de archivo como argumentos
    exportar_diccionario_a_excel(diccionario_por_propietario, claves_ordenadas)

    




