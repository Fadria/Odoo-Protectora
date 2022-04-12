# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from uuid import uuid4
from datetime import date

# Clase del controlador web
class ApiRest(http.Controller):

    '''
        Función usada para realizar login. Recibirá un usuario, su contraseña y devolverá un token de acceso o un mensaje de error
    '''
    @http.route('/apirest/login', auth="none", cors='*', csrf=False,
            methods=["POST"], type='http')
    def login(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos  = json.loads(args['data'])

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

                        # Enviamos una respuesta que contendrá el token y el estado OK
                        return http.Response( 
                        json.dumps({"token": str(token), "estado": "ok"}, default=str), 
                            status=200,
                            mimetype='application/json'
                        )

        # Enviamos una respuesta que contendrá el estado error, ya que no se ha podido iniciar sesión
        return http.Response( 
        json.dumps({"estado": "error"}, default=str), 
            status=200,
            mimetype='application/json'
        )