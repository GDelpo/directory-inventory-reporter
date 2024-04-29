import datetime
import pandas as pd

from logger import info_logger
from utils import obtener_listado_archivos

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
    
    # Volver a formatear la columna 'fecha_modificacion' al formato 'dd-mm-año' para el usuario final
    con_propietario['fecha_modificacion'] = con_propietario['fecha_modificacion'].dt.strftime('%d-%m-%Y')

    # Usa groupby para dividir el DataFrame por propietario
    for propietario, grupo in con_propietario.groupby('propietario'):
        diccionario_por_propietario[propietario] = {
            "dataframe": grupo.copy(),
            "mail": None
        }

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
    
    for propietario, data in diccionario_por_propietario.items():
        if propietario not in ('totalizador', 'sin propietario'):
            num_filas = len(data['dataframe'])  # Accede al DataFrame dentro del diccionario por propietario
            if (data['dataframe']['peso_en_mbs'] != 0).any() and not data['dataframe'].empty:
                total_peso = data['dataframe']['peso_en_mbs'].sum()
            else:
                total_peso = 'Solo hay archivos sin peso asignado'
            lista_totalizador.append((propietario, num_filas, total_peso))
    
    totalizador_df = pd.DataFrame(lista_totalizador, columns=['Propietario', 'Cantidad de registros en total', 'Peso total en MB'])
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

def exportar_diccionario_a_excel(diccionario, orden_claves, nombre_archivo='static/informe_directorio.xlsx'):
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
            if clave == 'totalizador' or clave == 'sin propietario':
                dataframe = diccionario[clave]
            else:
                # Obtener el DataFrame para este propietario
                dataframe = diccionario[clave]["dataframe"]

            # Reemplazar los espacios en blanco en los nombres de las hojas por guiones bajos
            nombre_hoja = clave.replace(' ', '_')

            # Escribir el DataFrame en la hoja correspondiente
            dataframe.to_excel(escritor_excel, sheet_name=nombre_hoja, index=False)

def obtener_correo_usuario(diccionario_usuarios, nombres_a_buscar):
    """
    Esta función busca los correos electrónicos de los usuarios especificados en un diccionario.

    Args:
        diccionario_usuarios (dict): Un diccionario que contiene información de los usuarios.
        nombres_a_buscar (list): Una lista de nombres de usuarios a buscar.

    Returns:
        dict: Un diccionario actualizado con los correos electrónicos encontrados para los usuarios.
    """
    # Cargar el archivo .xlsx en un DataFrame (esto podría realizarse fuera de la función si se llama repetidamente)
    df_cuentas = pd.read_excel('./static/fuente/cuentas_red_mail.xlsx')

    for nombre_usuario in nombres_a_buscar:
        # Verificar si el nombre de usuario está presente en la columna 'samaccountname' del DataFrame
        if nombre_usuario in df_cuentas['samaccountname'].values:
            # Obtener el correo electrónico del usuario
            correo_usuario = str(df_cuentas[df_cuentas['samaccountname'] == nombre_usuario]["EmailAddress"].values[0]).lower()
            # Agregar el correo electrónico al diccionario de usuarios
            diccionario_usuarios.setdefault(nombre_usuario, {})["mail"] = correo_usuario
            
    return diccionario_usuarios

def filtrar_por_fecha(df, anios):
    """
    Filtra un DataFrame por fecha de modificación.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna 'fecha_modificacion'.
        anios (int): Número de años para filtrar el DataFrame.

    Returns:
        pandas.DataFrame: DataFrame filtrado con las filas cuya fecha de modificación
                          sea anterior a 'anios' años desde la fecha actual.
    """
    # Calcular la fecha límite (hoy menos 'años' años)
    fecha_limite = datetime.datetime.now() - datetime.timedelta(days=365 * anios)

    # Filtrar el DataFrame para mantener solo las filas con fecha de modificación anterior a la fecha límite
    df_filtrado = df[df['fecha_modificacion'] < fecha_limite]

    return df_filtrado

def generar_reporte_directorio(ruta_seleccionada, anios, fecha_limite):
    
    # Crear un logger para la información del proceso
    info_logger.info(f"Generando reporte para la ruta: {ruta_seleccionada}")
    info_logger.info(f"Fecha límite para la revisión: {fecha_limite}")
    info_logger.info(f"Años de antigüedad sobre la fecha de modificación: {anios}")

    # Obtener una lista de archivos de la ruta 
    lista_archivos = obtener_listado_archivos(ruta_seleccionada)

    # Crear un DataFrame a partir de la lista de diccionarios
    df_listado_archivos = pd.DataFrame(lista_archivos)

    # Filtramos el df original con la cantidad maxima de años que queremos obtener, caso que no se requiera dicho filtro se comenta esta linea.
    df_listado_archivos = filtrar_por_fecha(df_listado_archivos, anios)

    # Exportar la ruta de los archivos a un archivo CSV
    df_listado_archivos['nombre'].to_csv('static/fuente/nombre_archivos.csv', index=False)
    
    # Dividir el DataFrame por propietario
    diccionario_por_propietario = dividir_df_por_propietario(df_listado_archivos)

    # Obtener las claves ordenadas del diccionario
    claves_ordenadas = ordenar_claves(diccionario_por_propietario)

    # Obtenemos los correos de los usuarios presentes en el diccionario en base a un excel generado por Leo
    diccionario_por_propietario = obtener_correo_usuario(diccionario_por_propietario, claves_ordenadas)

    # Llamar al método exportar_diccionario_a_excel pasando el diccionario, las claves ordenadas y el nombre de archivo como argumentos
    exportar_diccionario_a_excel(diccionario_por_propietario, claves_ordenadas)

    return diccionario_por_propietario
    
    
    

    




