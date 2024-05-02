import datetime as dt

from mailer import descomponer_diccionario, enviar_correos_a_personas
from procesador import generar_reporte_directorio
from logger import info_logger

def main(ruta_seleccionada):

    AÑOS = 2
    FECHA_LIMITE = (dt.datetime.now() + dt.timedelta(days=30)).strftime('%d-%m-%Y')
   #ruta_seleccionada = 'C:/Users/Usuario/Desktop/Prueba' # Ruta de la carpeta a analizar 

    diccionario = generar_reporte_directorio(ruta_seleccionada, AÑOS, FECHA_LIMITE)

    lista_correos_a_enviar = descomponer_diccionario(diccionario, ruta_seleccionada, AÑOS, FECHA_LIMITE)

    if lista_correos_a_enviar.__len__() > 0:
        enviar_correos_a_personas(lista_correos_a_enviar)
    
    info_logger.info(f"{'-'*50}")
    
