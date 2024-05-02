import csv
import os
import shutil

from logger import info_logger, error_logger

def cargar_rutas_desde_csv(archivo_csv):
    rutas = []
    with open(archivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            rutas.append(row[0])
    return rutas

def mover_rutas(ruta_seleccionada, rutas, ruta_nueva):
    ruta_seleccionada = os.path.abspath(ruta_seleccionada)
    ruta_nueva = os.path.abspath(ruta_nueva)
    for ruta in rutas:
        ruta_actual_completa = os.path.join(ruta_seleccionada, ruta)
        ruta_nueva_completa = os.path.join(ruta_nueva, ruta)
        if os.path.exists(ruta_actual_completa):
            try:
                if os.path.isfile(ruta_actual_completa):
                    shutil.copy2(ruta_actual_completa, ruta_nueva_completa)  # Copiar el archivo
                    os.remove(ruta_actual_completa)  # Eliminar el archivo original (opcional)
                else:
                    shutil.copytree(ruta_actual_completa, ruta_nueva_completa)  # Copiar el directorio
                    shutil.rmtree(ruta_actual_completa)  # Eliminar el directorio original
                info_logger.info(f"Ruta movida: {ruta_actual_completa} -> {ruta_nueva_completa}")            
            except OSError as e:
                error_logger.error(f"Error al mover la ruta: {e}")
            except Exception as e:
                error_logger.error(f"Error al mover la ruta: {e}")
        else:
            error_logger.error(f"La ruta no existe: {ruta_actual_completa}")
    
        
# Ruta del archivo CSV con las rutas originales
archivo_csv = 'static/fuente/nombre_archivos.csv'

# Ruta nueva donde se moverán las rutas
ruta_nueva = 'C:/Users/gdelponte/Desktop/prueba_directorio'
ruta_seleccionada = 'G:/Public'

# Cargar las rutas desde el archivo CSV
rutas = cargar_rutas_desde_csv(archivo_csv)

# Mover las rutas a la nueva ubicación
mover_rutas(ruta_seleccionada, rutas, ruta_nueva)

info_logger.info(f"{'-'*50}")