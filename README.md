# README - Proyecto de Generación de Informes de Directorios

Este proyecto consta de dos archivos principales: `main.py` y `procesador.py`. Su objetivo es permitir a los usuarios seleccionar un directorio en su sistema de archivos y generar un informe detallado de los archivos contenidos en ese directorio, organizados por propietario y otros detalles relevantes. A continuación, se describen los componentes y la funcionalidad del proyecto:

## Estructura de Archivos
- `main.py`: Este archivo contiene la interfaz de usuario desarrollada con la biblioteca `tkinter` de Python. Permite al usuario seleccionar un directorio y lanzar el proceso de generación del informe.
- `procesador.py`: En este archivo se encuentra la lógica principal para la generación del informe. Se encarga de obtener información sobre los archivos en el directorio seleccionado, incluyendo detalles como el propietario, la fecha de modificación y el tipo de archivo. Además, organiza esta información y la exporta a un archivo de Excel.

## Funcionalidad
El proyecto permite al usuario realizar las siguientes acciones:

1. Seleccionar un directorio en el sistema de archivos a través de la interfaz de usuario.
2. Generar un informe que incluye información detallada de los archivos en el directorio seleccionado, organizados por propietario y otros detalles relevantes.
3. Exportar este informe a un archivo de Excel con hojas separadas para cada propietario, incluyendo una hoja adicional para archivos sin propietario definido.

## Uso del Proyecto
Para utilizar el proyecto, siga los siguientes pasos:

1. Ejecute el archivo `main.py`. Esto abrirá la interfaz de usuario.
2. Haga clic en el botón "Elegir Ruta" para seleccionar el directorio del cual desea generar el informe.
3. Una vez seleccionado el directorio, el botón "Lanzar Informe" estará habilitado. Haga clic en este botón para generar el informe.
4. El informe se generará en un archivo de Excel llamado "informe_directorio.xlsx" y se organizará por propietario y otros detalles relevantes.

## Requisitos
El proyecto requiere la instalación de las siguientes bibliotecas de Python:

- `tkinter`: Para la interfaz de usuario.
- `pandas`: Para el manejo de datos y generación del informe en Excel.
- `win32security`: Para obtener información sobre el propietario de los archivos en sistemas Windows.

Puede instalar estas bibliotecas a través de la herramienta `pip` si aún no están instaladas.

## Personalización
El proyecto se puede personalizar según las necesidades específicas. Por ejemplo, puede modificar la lógica de organización de archivos en el informe o cambiar el nombre del archivo de salida. También puede personalizar el formato del informe en Excel según sus preferencias.

## Problemas Conocidos
El proyecto maneja adecuadamente errores como archivos no encontrados o permisos insuficientes y registra estos errores en un archivo de registro llamado "error.log". Si encuentra problemas durante el uso, consulte este archivo para obtener más detalles sobre los errores.

¡Gracias por utilizar este proyecto! Si tiene alguna pregunta o desea realizar mejoras, no dude en modificar el código o ponerse en contacto con el desarrollador."# pyhton_reporte_direcotrio" 
