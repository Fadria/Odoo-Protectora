# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime

class Revisiones(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'revisiones'
    _description = 'Revisiones de la protectora'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'fecha desc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS

    fecha = fields.Datetime("Fecha y hora de la revisión", required=True)
    animal = fields.Many2one('animales', store=True, required=True)
    voluntario = fields.Many2one('usuarios', store=True, required=True)
    observaciones = fields.Html('Observaciones', sanitize=True, strip_style=False, required=True)

    # FUNCIONES
    
    # Función usada para comprobar que la fecha no es posterior a la actual
    @api.constrains('fecha')
    def comprobar_fecha_revision(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si la fecha del registro es posterior a la actual lanzaremos una excepción
            if record.fecha > datetime.now():
                raise models.ValidationError('La fecha de publicación debe ser anterior a la actual')

    # Función usada para comprobar que en el campo voluntario se ha asignado una persona con el rol voluntario
    @api.constrains('voluntario')
    def comprobar_voluntario(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si el usuario no es un voluntario lanzaremos una excepción
            if record.voluntario.rol != "voluntario":
                raise models.ValidationError('La persona que realiza la revisión debe ser un voluntario')