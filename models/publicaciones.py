# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

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
    fechaPublicacion = fields.Datetime("Fecha y hora de la publicación")
    titulo = fields.Char("Título de la publicación")
    contenido = fields.Html('Contenido', sanitize=True, strip_style=False)
    autor = fields.Many2one("usuarios", "Autor") # Relación con el modelo de usuarios