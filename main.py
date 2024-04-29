# Definir la cantidad de años de antigüedad para filtrar los archivos
from mailer import descomponer_diccionario, enviar_correos_a_personas
from procesador import generar_reporte_directorio
import datetime as dt

def main(ruta_seleccionada):

    AÑOS = 2
    FECHA_LIMITE = (dt.datetime.now() + dt.timedelta(days=30)).strftime('%d-%m-%Y')
   #ruta_seleccionada = 'C:/Users/Usuario/Desktop/Prueba'

    diccionario = generar_reporte_directorio(ruta_seleccionada, AÑOS, FECHA_LIMITE)

    lista_correos_a_enviar = descomponer_diccionario(diccionario, ruta_seleccionada, AÑOS, FECHA_LIMITE)

    if lista_correos_a_enviar.__len__() > 0:
        enviar_correos_a_personas(lista_correos_a_enviar)

    
