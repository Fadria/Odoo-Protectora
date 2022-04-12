# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web
class ApiRest(http.Controller):
    @http.route('/apirest/login', auth="none", cors='*', csrf=False,
            methods=["POST"], type='http')
    def login(self, **args):
        # Cargamos los datos recibidos en la petición
        dicDatos  = json.loads(args['data'])

        if "usuario" in dicDatos and "contrasenya" in dicDatos:
            # Obtenemos una lista de usuarios que cumplan con la búsqueda
            bdData = http.request.env["usuarios"].sudo().search([('usuario', '=', dicDatos["usuario"])])

            # Comprobamos si el tamaño de la lista es mayor de 0, en el caso de que encontremos un resultado
            if len(bdData) > 0:
                # Obtenemos los datos del usuario
                usuario = bdData.read()[0]

                # Si la contraseña es correcta devolveremos un token de acceso
                if usuario["contrasenya"] == dicDatos["contrasenya"]:

                    # TODO GENERAR EL TOKEN Y ALMACENARLO EN LA ENTIDAD DEL USUARIO PARA VALIDARLO EN EL ENDPOINT CHECK_TOKEN
                    return "{'token':'WIP: generador de token'}"

            return "{'estado':'error'}"
        else:
            return "{'estado':'error'}"