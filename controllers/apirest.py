# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from uuid import uuid4
from datetime import date
import datetime

# Clase del controlador web
class ApiRest(http.Controller):

    ip = "http://192.168.1.135:8069"

    '''
        Función usada para realizar login. Recibirá un usuario, su contraseña y devolverá un token de acceso o un mensaje de error
    '''
    @http.route('/apirest/login', auth="none", cors='*', csrf=False,
            methods=["POST"], type='http')
    def login(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos = json.loads(args['data'])

        if "usuario" in dicDatos and "contrasenya" in dicDatos:
            # Obtenemos una lista de usuarios que cumplan con la búsqueda
            record = http.request.env["usuarios"].sudo().search([('usuario', '=', dicDatos["usuario"])])

            # Comprobamos que se ha encontrado al menos un usuario
            if record and record[0]:
                for usuario in record:
                    # Si la contraseña es correcta devolveremos un token de acceso
                    if usuario["contrasenya"] == dicDatos["contrasenya"]:

                        # Generamos un token para que el usuario pueda iniciar sesión automáticamente en posteriores ocasiones
                        token = uuid4()
                        
                        # Sobreescribimos el token y la fecha de caducidad de este en el registro del usuario
                        usuario.token = token
                        usuario.tokenCaducidad = date.today()

                        # Preparamos la respuesta a enviar
                        diccionarioRespuesta = {} # Diccionario de la respuesta
                        diccionarioRespuesta["token"] = token # Se almacenará en el teléfono para evitar loguearse en 30 días
                        diccionarioRespuesta["usuario"] = usuario.usuario # Nombre del usuario
                        diccionarioRespuesta["rol"] = usuario.rol # Rol del usuario
                        # Añadimos la url de la foto del usuario a la respuesta
                        diccionarioRespuesta["foto"] = self.ip + "/web/image?model=usuarios&id=" + str(usuario.id) + "&field=foto"

                        # Enviamos una respuesta que contendrá los datos del usuario necesarios y el estado ok
                        return http.Response( 
                        json.dumps({"data": diccionarioRespuesta, "estado": "ok"}, default=str), 
                            status=200,
                            mimetype='application/json'
                        )

        # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido iniciar sesión
        return http.Response( 
            json.dumps({"estado": "error"}, default=str), 
                status=200,
                mimetype='application/json'
        )

    '''
        Función usada para registrar un usuario
    '''
    @http.route('/apirest/registro', auth="none", cors='*', csrf=False,
                methods=["POST"], type='http')
    def registro(self, **args):
        try:
            # Cargamos los datos recibidos en la petición
            dicDatos = json.loads(args['data'])

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
            diccionarioRespuesta = {} # Diccionario de la respuesta
            diccionarioRespuesta["token"] = token # Se almacenará en el teléfono para evitar loguearse en 30 días
            diccionarioRespuesta["usuario"] = record.usuario # Nombre del usuario
            diccionarioRespuesta["rol"] = record.rol # Rol del usuario
            # Añadimos la url de la foto del usuario a la respuesta
            diccionarioRespuesta["foto"] = self.ip + "/web/image?model=usuarios&id=" + str(record.id) + "&field=foto"

            # Enviamos una respuesta que contendrá los datos del usuario necesarios y el estado ok
            return http.Response(
                    json.dumps({"data": diccionarioRespuesta, "estado": "ok"}, default=str),
                        status=200,
                        mimetype='application/json'
                )
        except:
            # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido crear el usuario
            return http.Response( 
                json.dumps({"estado": "error"}, default=str), 
                    status=200,
                    mimetype='application/json'
            )