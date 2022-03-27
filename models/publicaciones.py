# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime

class Publicaciones(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'publicaciones'
    _description = 'Publicaciones de los voluntarios'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'fechaPublicacion desc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS

    imagenPortada = fields.Image("Imagen de portada")
    fechaPublicacion = fields.Datetime("Fecha y hora de la publicación", required=True)
    titulo = fields.Char("Título de la publicación", required=True)
    contenido = fields.Html('Contenido', sanitize=True, strip_style=False, required=True)
    autor = fields.Many2one("usuarios", "Autor", required=True) # Relación con el modelo de usuarios

    # FUNCIONES

    # Función usada para comprobar que la fecha no es posterior a la actual
    @api.constrains('fechaPublicacion')
    def comprobar_fecha_publicacion(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si la fecha del registro es posterior a la actual lanzaremos una excepción
            if record.fechaPublicacion > datetime.now():
                raise models.ValidationError('La fecha de publicación debe ser anterior a la actual')
