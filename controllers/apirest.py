# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json # Manejo del formato JSON
from uuid import uuid4 # Generación de token

# Librerías relacionadas con la fecha
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta # Librería con la que podremos añadir días a una fecha

# Librerías usadas para enviar emails
import smtplib
from email.mime.text import MIMEText

# Librería usada para desordenar listas
import random

# Clase del controlador web
class ApiRest(http.Controller):

    # IP de nuestro servidor Odoo
    ip = "http://192.168.1.134:8069"

    # Función usada para realizar un login
    @http.route('/apirest/login', auth="none", cors='*', csrf=False,
            methods=["POST"], type='json')
            
    def login(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]

        diccionarioRespuesta = {} # Diccionario de la respuesta

        if "email" in dicDatos and "contrasenya" in dicDatos:
            # Obtenemos una lista de usuarios que cumplan con la búsqueda
            record = http.request.env["usuarios"].sudo().search([('email', '=', dicDatos["email"])])

            # Comprobamos que se ha encontrado al menos un usuario
            if record and record[0]:
                for usuario in record:
                    # Si la contraseña es correcta devolveremos un token de acceso
                    if usuario["contrasenya"] == dicDatos["contrasenya"]:

                        # Generamos un token para que el usuario pueda iniciar sesión automáticamente en posteriores ocasiones
                        token = uuid4()
                        
                        # Sobreescribimos el token y la fecha de caducidad de este en el registro del usuario
                        usuario.token = token
                        usuario.tokenCaducidad = date.today() + relativedelta(months=+1) # El token caducará en un mes

                        # Preparamos la respuesta a enviar
                        diccionarioRespuesta["token"] = usuario.token # Se almacenará en el teléfono para evitar loguearse en 30 días
                        diccionarioRespuesta["usuario"] = usuario.usuario # Nombre del usuario
                        diccionarioRespuesta["rol"] = usuario.rol # Rol del usuario
                        
                        # Añadimos la url de la foto del usuario a la respuesta
                        diccionarioRespuesta["foto"] = self.ip + "/web/image?model=usuarios&id=" + str(usuario.id) + "&field=foto"
                        
                        # Indicamos el estado del resultado
                        diccionarioRespuesta["status"] = "ok"

                        # Devolvemos la respuesta en el formato cadena
                        return str(diccionarioRespuesta)

        # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido iniciar sesión
        diccionarioRespuesta["status"] = "error"
        return str(diccionarioRespuesta)

    # Función usada para realizar un login
    @http.route('/apirest/loginToken', auth="none", cors='*', csrf=False,
            methods=["POST"], type='json')
            
    def loginToken(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]

        diccionarioRespuesta = {} # Diccionario de la respuesta

        if "token" in dicDatos:
            # Obtenemos una lista de usuarios que cumplan con la búsqueda
            record = http.request.env["usuarios"].sudo().search([('token', '=', dicDatos["token"])])

            # Comprobamos que se ha encontrado al menos un usuario
            if record and record[0]:
                for usuario in record:

                    today = date.today()
                    if usuario.tokenCaducidad > today:
                        # Preparamos la respuesta a enviar
                        diccionarioRespuesta["usuario"] = usuario.usuario # Nombre del usuario
                        diccionarioRespuesta["rol"] = usuario.rol # Rol del usuario
                        
                        # Añadimos la url de la foto del usuario a la respuesta
                        diccionarioRespuesta["foto"] = self.ip + "/web/image?model=usuarios&id=" + str(usuario.id) + "&field=foto"
                        
                        # Indicamos el estado del resultado
                        diccionarioRespuesta["status"] = "ok"

                        # Devolvemos la respuesta en el formato cadena
                        return str(diccionarioRespuesta)

        # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido iniciar sesión
        diccionarioRespuesta["status"] = "error"
        return str(diccionarioRespuesta)

    # Función usada para realizar un registro
    @http.route('/apirest/registro', auth="none", cors='*', csrf=False,
                methods=["POST"], type='json')
    def registro(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Cargamos los datos recibidos en la petición
            dicDatos = json.loads(request.httprequest.data)
            dicDatos = dicDatos["data"]

            # Comprobamos si el email está en uso
            record = http.request.env["usuarios"].sudo().search([('email', '=', dicDatos["email"])])

            # Está en uso, devolvemos un error
            if record and record[0]:
                diccionarioRespuesta["status"] = "emailUsado"
                return str(diccionarioRespuesta)


            # Comprobamos si el usuario está en uso
            record = http.request.env["usuarios"].sudo().search([('usuario', '=', dicDatos["usuario"])])

            # Está en uso, devolvemos un error
            if record and record[0]:
                diccionarioRespuesta["status"] = "usuarioUsado"
                return str(diccionarioRespuesta)

            # Damos el formato necesario a la fecha de nacimiento
            dicDatos["fechaNacimiento"] = datetime.datetime.strptime(dicDatos["fechaNacimiento"], '%Y-%m-%d')

            # Por seguridad, indicaremos que el rol es Adoptante, para evitar que en el request podamos recibir otro rol superior
            dicDatos["rol"] = "adoptante"

            # Creamos el usuario y obtenemos todos sus valores (la id generada, por ejemplo)
            record = request.env["usuarios"].sudo().create(
                # Indicamos el diccionario que usaremos para crear el registro
                dicDatos
            )

            # Generamos un token para que el usuario pueda iniciar sesión automáticamente en posteriores ocasiones
            token = uuid4()
            
            # Sobreescribimos el token y la fecha de caducidad de este en el registro del usuario
            record.token = token
            record.tokenCaducidad = date.today()

            # Preparamos la respuesta a enviar
            diccionarioRespuesta["token"] = record.token # Se almacenará en el teléfono para evitar loguearse en 30 días
            diccionarioRespuesta["usuario"] = record.usuario # Nombre del usuario
            diccionarioRespuesta["rol"] = record.rol # Rol del usuario

            # Enviamos una respuesta que contendrá los datos del usuario necesarios y el estado ok
            # Indicamos el estado del resultado
            diccionarioRespuesta["status"] = "ok"

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)
        except:
            # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido crear el usuario
            # Indicamos el estado del resultado
            diccionarioRespuesta["status"] = "error"

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)


    # Función usada para recuperar la contraseña
    @http.route('/apirest/recuperarContrasenya', auth="none", cors='*', csrf=False,
                methods=["POST"], type='json')
    def recuperarContrasenya(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]
        
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Recuperamos el usuario al que cambiar la contraseña
            record = http.request.env["usuarios"].sudo().search([('email', '=', dicDatos["email"])])
            record.contrasenya = uuid4()

            html = ("""\
            <html>
            <body>
                <h1>Solicitud de recuperación de contraseña</h1>
                <p>Saludos, """ +  record.usuario + """, has recibido este correo electrónico porque has olvidado tu contraseña de la aplicación NuevoLazo. Si piensas que has recibido este correo electrónico por equivocación, contacta con nosotros a través de fadriacarrasco@gmail.com</p>
                <p>Ya no podrás iniciar sesión en tu cuenta con la contraseña antigua. Para restablecer la contraseña, accede a la aplicación con la contraseña """ + record.contrasenya + """, donde puedes cambiarla desde la sección de Mi Perfil.</p>
            </body>
            </html>
            """)

            msg = MIMEText(html, "html")
            msg['Subject'] = "Solicitud de recuperación de contraseña"
            msg['From']    = "postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org"
            msg['To']      = record.email

            s = smtplib.SMTP('smtp.mailgun.org', 587)

            s.login('postmaster@sandbox0d79cad6a2f0428b890f0244f1865b7a.mailgun.org', '05dfa61f485be672ccda8e7a0e5724bb-162d1f80-2641c3f7')
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()        

            # Enviamos una respuesta que contendrá el estado ok
            diccionarioRespuesta["status"] = "ok"
            return str(diccionarioRespuesta)

        except:
            # Enviamos una respuesta que contendrá el estado error, ya que no se ha encontrado el email del usuario
            diccionarioRespuesta["status"] = "error"
            return str(diccionarioRespuesta)

    # Función usada para realizar un logout
    @http.route('/apirest/logout', auth="none", cors='*', csrf=False,
                methods=["POST"], type='json')
    def logout(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]

        diccionarioRespuesta = {} # Diccionario de la respuesta

        if "token" in dicDatos:
            # Obtenemos una lista de usuarios que cumplan con la búsqueda
            record = http.request.env["usuarios"].sudo().search([('token', '=', dicDatos["token"])])

            # Comprobamos que se ha encontrado al menos un usuario
            if record and record[0]:
                for usuario in record:
                    # Sobreescribimos el token y la fecha de caducidad y los dejamos sin valor
                    usuario.token = None
                    usuario.tokenCaducidad = None
                    
                    # Indicamos el estado del resultado
                    diccionarioRespuesta["status"] = "ok"

                    # Devolvemos la respuesta en el formato cadena
                    return str(diccionarioRespuesta)

        # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido iniciar sesión
        diccionarioRespuesta["status"] = "error"
        return str(diccionarioRespuesta)

    # Función que nos devolverá el listado de publicaciones
    @http.route('/apirest/publicaciones', auth="none", cors='*', csrf=False,
                methods=["GET"], type='http')
    def publicaciones(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaPublicaciones = [] # Listado de publicaciones

        # Obtenemos una lista de usuarios que cumplan con la búsqueda
        record = http.request.env["publicaciones"].sudo().search([])

        # Comprobamos que se ha encontrado al menos una publicación
        if record and record[0]:
            for publicacion in record:
                # Inicializamos el diccionario que contendrá los datos de la publicación
                diccionarioPublicacion = {}

                # Indicamos sus valores
                diccionarioPublicacion["id"] = publicacion.id
                diccionarioPublicacion["titulo"] = publicacion.titulo[0:20] + "..."
                diccionarioPublicacion["fechaPublicacion"] = publicacion.fechaPublicacion.strftime("%d/%m/%y")
                diccionarioPublicacion["imagenPortada"] = self.ip + "/web/image?model=publicaciones&id=" + str(publicacion.id) + "&field=imagenPortada"
                diccionarioPublicacion["autor"] = publicacion.autor.nombreCompleto
                diccionarioPublicacion["contenido"] = publicacion.contenido[0:35] + "..."

                # La añadimos al listado
                listaPublicaciones.append(diccionarioPublicacion)                                
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = listaPublicaciones

        # Devolvemos la respuesta en el formato cadena
        return str(diccionarioRespuesta)

    # Función que nos devolverá los datos de una publicación
    @http.route('/apirest/publicaciones/<idPublicacion>', auth="none", cors='*', csrf=False,
                methods=["GET"], type='http')
    def obtenerPublicacion(self, idPublicacion, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaPublicaciones = [] # Listado de publicaciones

        # Obtenemos una lista de usuarios que cumplan con la búsqueda
        record = http.request.env["publicaciones"].sudo().search([("id", "=", idPublicacion)])

        # Comprobamos que se ha encontrado al menos una publicación
        if record and record[0]:
            for publicacion in record:
                # Inicializamos el diccionario que contendrá los datos de la publicación
                diccionarioPublicacion = {}

                # Indicamos sus valores
                diccionarioPublicacion["titulo"] = publicacion.titulo
                diccionarioPublicacion["fechaPublicacion"] = publicacion.fechaPublicacion.strftime("%d/%m/%y")
                diccionarioPublicacion["imagenPortada"] = self.ip + "/web/image?model=publicaciones&id=" + str(publicacion.id) + "&field=imagenPortada"
                diccionarioPublicacion["autor"] = publicacion.autor.nombreCompleto
                diccionarioPublicacion["contenido"] = publicacion.contenido

                # La añadimos al listado
                listaPublicaciones.append(diccionarioPublicacion)                                
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = listaPublicaciones

        # Devolvemos la respuesta en el formato cadena
        return str(diccionarioRespuesta)

    # Función que nos devolverá el listado de gráficos
    @http.route('/apirest/graficos', auth="none", cors='*', csrf=False,
                methods=["GET"], type='http')
    def graficos(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaGraficos = [] # Listado de gráficos

        # Obtenemos una lista de usuarios que cumplan con la búsqueda
        record = http.request.env["graficos"].sudo().search([])

        # Comprobamos que se ha encontrado al menos un gráfico
        if record and record[0]:
            for grafico in record:
                # Inicializamos el diccionario que contendrá los datos del gráfico
                diccionarioGrafico = {}

                # Indicamos sus valores
                diccionarioGrafico["imagen"] = self.ip + "/web/image?model=graficos&id=" + str(grafico.id) + "&field=imagen"
                diccionarioGrafico["titulo"] = grafico.titulo
                diccionarioGrafico["fecha"] = grafico.fecha.strftime("%d/%m/%y")

                # La añadimos al listado
                listaGraficos.append(diccionarioGrafico)                                
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = listaGraficos

        # Devolvemos la respuesta en el formato cadena
        return str(diccionarioRespuesta)        

    # Función que nos devolverá los datos de una publicación
    @http.route('/apirest/revisiones/<idAnimal>', auth="none", cors='*', csrf=False,
                methods=["GET"], type='http')
    def obtenerRevisiones(self, idAnimal, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaRevisiones = [] # Listado de revisiones

        # Obtenemos la lista de revisiones del animal
        record = http.request.env["revisiones"].sudo().search([("animal.id", "=", idAnimal)])

        # Comprobamos que se ha encontrado al menos una revisión
        if record and record[0]:
            for revision in record:
                # Inicializamos el diccionario que contendrá los datos de la revisión
                diccionarioRevision = {}

                # Indicamos sus valores
                diccionarioRevision["idAnimal"] = revision.animal.id
                diccionarioRevision["nombreVoluntario"] = revision.voluntario.nombreCompleto
                diccionarioRevision["fecha"] = revision.fecha.strftime("%d/%m/%y")
                diccionarioRevision["observaciones"] = revision.observaciones

                # La añadimos al listado
                listaRevisiones.append(diccionarioRevision)                                
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = listaRevisiones

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)      

        diccionarioRespuesta["status"] = "vacio"
        return str(diccionarioRespuesta)

    # Función usada para crear un nuevo registro
    @http.route('/apirest/nuevaRevision', auth="none", cors='*', csrf=False,
                methods=["POST"], type='json')
    def nuevaRevision(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Cargamos los datos recibidos en la petición
            dicDatos = json.loads(request.httprequest.data)
            dicDatos = dicDatos["data"]

            # COMPROBAR SI EL TOKEN PERTENECE A UN USUARIO VOLUTARIO

            # Comprobamos si el token pertenece a un voluntario
            usuario = http.request.env["usuarios"].sudo().search([('token', '=', dicDatos["token"])])

            # No es voluntario, devolvemos el diccionario vacío
            if usuario and usuario[0] and usuario[0].rol != "voluntario":
                return str(diccionarioRespuesta)

            # Preparamos el objeto a crear
            dicRevision = {}
            dicRevision["fecha"] = dicDatos["fecha"]
            dicRevision["animal"] = dicDatos["id"]
            dicRevision["observaciones"] = dicDatos["observaciones"]
            dicRevision["voluntario"] = usuario.id

            # Creamos la revisión
            request.env["revisiones"].sudo().create(
                # Indicamos el diccionario que usaremos para crear la revisión
                dicRevision
            )

            # Indicamos el estado del resultado
            diccionarioRespuesta["status"] = "ok"

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)
        except:
            # Indicamos el estado del resultado
            diccionarioRespuesta["status"] = "error"

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)        

    # Función que nos devolverá el listado de animales
    @http.route('/apirest/animales', auth="none", cors='*', csrf=False,
                methods=["GET"], type='http')
    def animales(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaAnimales = [] # Listado de animales

        # Obtenemos una lista de animales
        record = http.request.env["animales"].sudo().search([])

        # Comprobamos que se ha encontrado al menos un animal
        if record and record[0]:
            for animal in record:
                # Inicializamos el diccionario que contendrá los animales
                diccionarioAnimal = {}

                # Indicamos sus valores
                diccionarioAnimal["id"] = animal.id
                diccionarioAnimal["nombre"] = animal.nombre
                diccionarioAnimal["imagen"] = self.ip + "/web/image?model=animales&id=" + str(animal.id) + "&field=imagen"
                diccionarioAnimal["especie"] = animal.especie.capitalize()
                diccionarioAnimal["edad"] = animal.edad
                diccionarioAnimal["sexo"] = animal.sexo
                diccionarioAnimal["tamanyo"] = animal.tamanyo if animal.tamanyo != "pequenyo" else "pequeño"

                # La añadimos al listado
                listaAnimales.append(diccionarioAnimal)                                
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Desordenamos la lista de animales para impedir que se discriminen según cuándo se dieron de alta en el sistema
            random.shuffle(listaAnimales)

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = listaAnimales

        # Devolvemos la respuesta en el formato cadena
        return str(diccionarioRespuesta).replace("'", '"')

    # Función que nos devolverá el listado de animales filtrados
    @http.route('/apirest/filtrarAnimales', auth="none", cors='*', csrf=False,
                methods=["POST"], type='json')
    def filtrarAnimales(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaAnimales = [] # Listado de animales

        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]

        buscarDatos = True # Variable que cambiaremos a false cuando no sea necesario realizar más consultas

        # Obtenemos una lista de animales
        record = http.request.env["animales"].sudo().search([ ('especie', '=', dicDatos["especie"]), ('sexo', '=', dicDatos["sexo"]), ('tamanyo', '=', dicDatos["tamanyo"]) ])            

        # Comprobamos que se ha encontrado al menos un animal
        if record and record[0]:
            for animal in record:
                # Inicializamos el diccionario que contendrá los animales
                diccionarioAnimal = {}

                # Indicamos sus valores
                diccionarioAnimal["id"] = animal.id

                # La añadimos al listado
                listaAnimales.append(diccionarioAnimal)                                
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Desordenamos la lista de animales para impedir que se discriminen según cuándo se dieron de alta en el sistema
            random.shuffle(listaAnimales)

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = listaAnimales

        # Devolvemos la respuesta en el formato cadena
        return str(diccionarioRespuesta)

    # Función que nos devolverá los datos de un animal
    @http.route('/apirest/animales/<id>', auth="none", cors='*', csrf=False,
                methods=["GET"], type='http')
    def datosAnimal(self, id, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta
        listaDatos = [] # Listado que contendrá los datos del animal

        # Obtenemos la lista de revisiones del animal
        record = http.request.env["animales"].sudo().search([("id", "=", id)])

        # Comprobamos que se ha encontrado un animal
        if record and record[0]:
            for animal in record:
                # Inicializamos el diccionario que contendrá los datos del animal
                diccionarioAnimal = {}

                # Indicamos sus valores
                diccionarioAnimal["id"] = animal.id
                diccionarioAnimal["nombre"] = animal.nombre
                diccionarioAnimal["imagen"] = self.ip + "/web/image?model=animales&id=" + str(animal.id) + "&field=imagen"
                diccionarioAnimal["chip"] = "Chipeado" if animal.chip == True else "No chipeado"
                diccionarioAnimal["especie"] = animal.especie.capitalize()
                diccionarioAnimal["raza"] = animal.raza if animal.raza != False else "Sin raza"
                diccionarioAnimal["nacimiento"] = animal.nacimiento.strftime("%d/%m/%y")
                diccionarioAnimal["edad"] = animal.edad
                diccionarioAnimal["sexo"] = animal.sexo
                diccionarioAnimal["tamanyo"] = animal.tamanyo if animal.tamanyo != "pequenyo" else "pequeño"
                diccionarioAnimal["urgente"] = "Si" if animal.urgente == True else "No"
                diccionarioAnimal["peso"] = animal.peso
                diccionarioAnimal["esterilizado"] = "Si" if animal.esterilizado == True else "No"
                diccionarioAnimal["exotico"] = "Si" if animal.exotico == True else "No"
                diccionarioAnimal["observaciones"] = animal.observaciones
                diccionarioAnimal["pelo"] = "Si" if animal.pelo == True else "No"
                diccionarioAnimal["historia"] = animal.historia
                diccionarioAnimal["perroPeligroso"] = "Si" if animal.perroPeligroso == True else "No"

                listaImagenes = [] # Lista donde guardaremos las imágenes del animal

                # Obtenemos las imágenes del animal
                imagenes = http.request.env["imagenes"].sudo().search([("animal.id", "=", id)])

                # Preparamos el diccionario con las imágenes
                if imagenes and imagenes[0]:
                    for imagen in imagenes:
                        diccionarioImagen = {}
                        diccionarioImagen["id"] = imagen.id
                        diccionarioImagen["fecha"] = imagen.fecha.strftime("%d/%m/%y")
                        diccionarioImagen["imagen"] = self.ip + "/web/image?model=imagenes&id=" + str(imagen.id) + "&field=imagen"

                        listaImagenes.append(diccionarioImagen)

                diccionarioAnimal["imagenes"] = listaImagenes
                
                # Indicamos el estado del resultado
                diccionarioRespuesta["status"] = "ok"

            # Añadimos el listado al diccionario de la respuesta
            diccionarioRespuesta["data"] = diccionarioAnimal

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta).replace("'", '"')      

        diccionarioRespuesta["status"] = "vacio"
        return str(diccionarioRespuesta)       

    # Función usada para obtener los datos de un usuario
    @http.route('/apirest/userData', auth="none", cors='*', csrf=False,
            methods=["POST"], type='json')
            
    def userData(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(request.httprequest.data)
        dicDatos = dicDatos["data"]

        diccionarioRespuesta = {} # Diccionario de la respuesta

        if "token" in dicDatos:
            # Obtenemos una lista de usuarios que cumplan con la búsqueda
            record = http.request.env["usuarios"].sudo().search([('token', '=', dicDatos["token"])])

            # Comprobamos que se ha encontrado al menos un usuario
            if record and record[0]:
                for usuario in record:
                    # Preparamos la respuesta a enviar
                    diccionarioRespuesta["usuario"] = usuario.usuario
                    diccionarioRespuesta["nombreCompleto"] = usuario.nombreCompleto
                    diccionarioRespuesta["rol"] = usuario.rol
                    diccionarioRespuesta["email"] = usuario.email
                    diccionarioRespuesta["telefono"] = usuario.telefono
                    diccionarioRespuesta["direccion"] = usuario.direccion
                    diccionarioRespuesta["ciudad"] = usuario.ciudad
                    diccionarioRespuesta["codigoPostal"] = usuario.codigoPostal
                    diccionarioRespuesta["permisoPPP"] = "Con permiso PPP" if usuario.permisoPPP == True else "Sin permiso PPP"
                    diccionarioRespuesta["fechaNacimiento"] =  usuario.fechaNacimiento.strftime("%d/%m/%y")

                    # Indicamos el estado del resultado
                    diccionarioRespuesta["status"] = "ok"

                    # Devolvemos la respuesta en el formato cadena
                    return str(diccionarioRespuesta)

        # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido iniciar sesión
        diccionarioRespuesta["status"] = "error"
        return str(diccionarioRespuesta)

    # Función usada para actualizar un usuario
    @http.route('/apirest/actualizarUsuario', auth="none", cors='*', csrf=False,
                methods=["PUT"], type='json')
    def actualizarUsuario(self, **args):
        diccionarioRespuesta = {} # Diccionario de la respuesta

        try:
            # Cargamos los datos recibidos en la petición
            dicDatos = json.loads(request.httprequest.data)
            dicDatos = dicDatos["data"]

            # Comprobamos si el token existe
            record = http.request.env["usuarios"].sudo().search([('token', '=', dicDatos["token"])])
            record = record[0]

            if "usuario" in dicDatos and record.usuario != dicDatos["usuario"]:
                # Comprobamos si el usuario está en uso
                userBD = http.request.env["usuarios"].sudo().search([('usuario', '=', dicDatos["usuario"])])

                # Está en uso, devolvemos un error
                if userBD and userBD[0]:
                    diccionarioRespuesta["status"] = "usuarioUsado"
                    return str(diccionarioRespuesta)
                record.usuario = dicDatos["usuario"]

            if "email" in dicDatos and record.email != dicDatos["email"]:
                # Comprobamos si el email está en uso
                emailBD = http.request.env["usuarios"].sudo().search([('email', '=', dicDatos["email"])])

                # Está en uso, devolvemos un error
                if emailBD and emailBD[0]:
                    diccionarioRespuesta["status"] = "emailUsado"
                    return str(diccionarioRespuesta)
                record.email = dicDatos["email"]
            
            if "nombreCompleto" in dicDatos: record.nombreCompleto = dicDatos["nombreCompleto"]
            if "contrasenya" in dicDatos:record.contrasenya = dicDatos["contrasenya"]
            if "telefono" in dicDatos: record.telefono = dicDatos["telefono"]
            if "direccion" in dicDatos: record.direccion = dicDatos["direccion"]
            if "ciudad" in dicDatos: record.ciudad = dicDatos["ciudad"]
            if "codigoPostal" in dicDatos: record.codigoPostal = dicDatos["codigoPostal"]
            if "fechaNacimiento" in dicDatos: record.fechaNacimiento = dicDatos["fechaNacimiento"]
            if "permisoPPP" in dicDatos: record.permisoPPP = dicDatos["permisoPPP"]

            # Indicamos el estado del resultado
            diccionarioRespuesta["status"] = "ok"

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)
        except:
            # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido actualizar el usuario
            # Indicamos el estado del resultado
            diccionarioRespuesta["status"] = "error"

            # Devolvemos la respuesta en el formato cadena
            return str(diccionarioRespuesta)