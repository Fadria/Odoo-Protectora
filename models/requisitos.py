# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime

class Requisitos(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'requisitos'
    _description = 'Requisitos y consejos anteriores a una adopción'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'id desc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS

    titulo = fields.Char("Título del requisito", required=True)
    contenido = fields.Text('Contenido', required=True)
    imagen = fields.Image("Imagen del requisito")