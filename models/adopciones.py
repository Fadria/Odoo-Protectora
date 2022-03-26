# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Adopciones(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'adopciones'
    _description = 'Adopciones de la protectora'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'fecha desc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS

    fecha = fields.Datetime("Fecha y hora de la adopción", required=True)
    animal = fields.Many2one('animales', store=True, required=True)
    dueño = fields.Many2one('usuarios', store=True, required=True)