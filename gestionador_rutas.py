import csv
import os

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
        try:
            os.rename(ruta_actual_completa, ruta_nueva_completa)
            print(f"Ruta movida: {ruta_actual_completa} -> {ruta_nueva_completa}")            
        except OSError as e:
            print(f"Error al mover la ruta: {e}")
        
# Ruta del archivo CSV con las rutas originales
archivo_csv = 'static/fuente/nombre_archivos.csv'

# Ruta nueva donde se moverán las rutas
ruta_nueva = 'C:/'
ruta_seleccionada = 'G:/Public'

# Cargar las rutas desde el archivo CSV
rutas = cargar_rutas_desde_csv(archivo_csv)

# Mover las rutas a la nueva ubicación
mover_rutas(ruta_seleccionada, rutas, ruta_nueva)