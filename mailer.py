from jinja2 import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from logger import error_logger, info_logger

def descomponer_diccionario(diccionario, ruta_seleccionada, años, fecha_limite):
    lista_correos_a_enviar = []
    for nombre, datos in diccionario.items():
        if nombre not in ['totalizador', 'sin_propietario']:
            correo_persona = datos.get('mail')
            if correo_persona:                
                # Obtener el DataFrame de los datos
                dataframe = datos['dataframe']
                # Convertir DataFrame a lista de diccionarios
                lista_datos = dataframe.to_dict(orient='records')
                # Crear un template con los datos
                html_correo = crear_template_con_datos(nombre, lista_datos, ruta_seleccionada, años, fecha_limite)
                # Agregar el correo y el HTML a la lista de correos a enviar
                lista_correos_a_enviar.append((correo_persona, html_correo))
                
    return lista_correos_a_enviar

def crear_template_con_datos(nombre, lista_datos, ruta_seleccionada, años, fecha_limite):
    # Crear un diccionario con todos los datos para la plantilla
    datos_plantilla = {
        'nombre_destinatario': nombre,
        'dataframe': lista_datos,
        'años': años,
        'ruta_seleccionada': ruta_seleccionada,
        'fecha_limite': fecha_limite
    }

    # Crear una instancia de la plantilla a partir del archivo
    with open('./static/plantilla_html/plantilla.html', 'r', encoding='utf-8') as file:
        template_html = file.read()
    
    # Crear una instancia de la plantilla
    template = Template(template_html)

    # Rellenar la plantilla con los datos
    html_formateado = template.render(datos_plantilla)

    return html_formateado

def enviar_correo(correo_persona, html_correo):
    # Inicializar la variable que indica si el correo se envió correctamente
    se_envio = False
    # Configurar los parámetros del correo pueden estar en un .env
    remitente = 'sistemas@nobleseguros.com'
    destinatario_cc = 'guido.delponte@nobleseguros.com'
    destinatario = correo_persona
    asunto = 'Informe de archivos en directorio compartido'
    # Crear el mensaje que se envia por mail
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Cc'] = destinatario_cc
    mensaje['Subject'] = asunto
    # Cuerpo del correo en formato HTML
    mensaje.attach(MIMEText(html_correo, "html"))
    try:
        #SMTP tiene que estar en un .env
        SMTP_IP = '192.168.190.98'
        # Crear conexión con el servidor de correo
        server = smtplib.SMTP(SMTP_IP, 25) #se usa el tipico que es el 25, podria tranquilamente venir del .env
        # Enviar correo
        server.sendmail(remitente, destinatario + ',' + destinatario_cc, mensaje.as_string())   
        # Cerrar la conexión con el servidor de correo
        server.quit()
        se_envio = True         
    except smtplib.SMTPConnectError:
        error_logger.error('Error: Unable to establish a connection with the SMTP server.')
    except smtplib.SMTPServerDisconnected:
        error_logger.error('Error: The SMTP server unexpectedly disconnected.')
    except smtplib.SMTPException as e:
        error_logger.error(f'Error al enviar el correo: {str(e)}')
    finally:
        return se_envio     
    
def enviar_correos_a_personas(lista_correos_a_enviar):
    enviados = 0
    for correo_persona, html_correo in lista_correos_a_enviar:
        se_envio = enviar_correo(correo_persona, html_correo)  # Llamar a la función enviar_correo
        if se_envio:
            enviados += 1
            info_logger.info(f'Correo enviado a: {correo_persona}')
    if enviados == len(lista_correos_a_enviar):
        info_logger.info(f'Correos enviados correctamente: {enviados} de {len(lista_correos_a_enviar)}')
        info_logger.info(f"{'-'*50}")        
    else:
        error_logger.error(f'Error al enviar correos. Correos enviados: {enviados} de {len(lista_correos_a_enviar)}')
