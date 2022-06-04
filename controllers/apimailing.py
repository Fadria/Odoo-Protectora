from odoo import http
from odoo.http import request

import json # Manejo del formato JSON

# Librerías usadas para enviar emails
import smtplib
from email.mime.text import MIMEText

# Clase usada para los endpoints relacionados con el envío de emails
class ApiMailing(http.Controller):

    # Endpoint usado para realizar el envío de un email para contactar con la protectora
    @http.route('/apirest/contacto', auth="none", cors='*', csrf=False,
                methods=["POST"], type='json')
    def recibirMensajeContacto(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]
        
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Variable que contendrá el HTML usado en el email
            html = ("""\
            <html>
            <body>
                <h1>Nuevo mensaje de contacto</h1>
                <p>Usuario: """ +  dicDatos["nombre"] +"""</p>
                <p>Email: """ +  dicDatos["email"] +"""</p>
                <p>Mensaje: """ +  dicDatos["mensaje"] +"""</p>
            </body>
            </html>
            """)

            # Preparación de los datos del email
            msg = MIMEText(html, "html") # Se indica el cuerpo, que contendrá el HTML definido anteriormente
            msg['Subject'] = "Nuevo Lazo | Solicitud de información"
            msg['From']    = "postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org"
            msg['To']      = "fadriacarrasco@gmail.com"

            # Indicamos el servidor a utilizar
            s = smtplib.SMTP('smtp.mailgun.org', 587)

            # Iniciamos sesión con las credenciales de cuenta
            s.login('postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org', '05dfa61f485be672ccda8e7a0e5724bb-162d1f80-2641c3f7')

            # Se envía el email y se cierra el servicio
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()        

            # Enviamos una respuesta que contendrá el estado ok
            diccionarioRespuesta["status"] = "ok"
            return str(diccionarioRespuesta)

        except:
            # Enviamos una respuesta que contendrá el estado error
            diccionarioRespuesta["status"] = "error"
            return str(diccionarioRespuesta)

    # Endpoint usado para realizar el envío de un email para solicitar información sobre un animal
    @http.route('/apirest/informacionAnimal', auth="none", csrf=False,
                methods=["POST"], type='json')
    def enviarSolicitudAnimal(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]
        
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Variable que contendrá el HTML usado en el email
            html = ("""\
            <html>
            <body>
                <h1>Solicitud de información</h1>
                <p>Email: """ +  dicDatos["email"] +"""</p>
                <p>Animal: """ + dicDatos["idAnimal"] + " " + dicDatos["nombre"] + """</p>
            </body>
            </html>
            """)

            # Preparación de los datos del email
            msg = MIMEText(html, "html") # Se indica el cuerpo, que contendrá el HTML definido anteriormente
            msg['Subject'] = "Nuevo Lazo | Solicitud animal"
            msg['From']    = "postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org"
            msg['To']      = "fadriacarrasco@gmail.com"

            # Indicamos el servidor a utilizar
            s = smtplib.SMTP('smtp.mailgun.org', 587)

            # Iniciamos sesión con las credenciales de cuenta
            s.login('postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org', '05dfa61f485be672ccda8e7a0e5724bb-162d1f80-2641c3f7')

            # Se envía el email y se cierra el servicio
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()        

            # Enviamos una respuesta que contendrá el estado ok
            diccionarioRespuesta["status"] = "ok"
            return str(diccionarioRespuesta)

        except:
            # Enviamos una respuesta que contendrá el estado error, ya que no se ha encontrado el email del usuario
            diccionarioRespuesta["status"] = "error"
            return str(diccionarioRespuesta)

    # Endpoint usado para realizar el envío de un email para solicitar formar parte del voluntariado
    @http.route('/apirest/informacionVoluntariado', auth="none", csrf=False,
                methods=["POST"], type='json')
    def recibirMensajeVoluntariado(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]
        
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Variable que contendrá el HTML usado en el email
            html = ("""\
            <html>
            <body>
                <h1>Solicitud de voluntariado</h1>
                <p>Email: """ +  dicDatos["email"] +"""</p>
            </body>
            </html>
            """)

            # Preparación de los datos del email
            msg = MIMEText(html, "html") # Se indica el cuerpo, que contendrá el HTML definido anteriormente
            msg['Subject'] = "Nuevo Lazo | Solicitud de voluntariado"
            msg['From']    = "postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org"
            msg['To']      = "fadriacarrasco@gmail.com"

            # Indicamos el servidor a utilizar
            s = smtplib.SMTP('smtp.mailgun.org', 587)

            # Iniciamos sesión con las credenciales de cuenta
            s.login('postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org', '05dfa61f485be672ccda8e7a0e5724bb-162d1f80-2641c3f7')

            # Se envía el email y se cierra el servicio
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()        

            # Enviamos una respuesta que contendrá el estado ok
            diccionarioRespuesta["status"] = "ok"
            return str(diccionarioRespuesta)

        except:
            # Enviamos una respuesta que contendrá el estado error, ya que no se ha encontrado el email del usuario
            diccionarioRespuesta["status"] = "error"
            return str(diccionarioRespuesta)
