# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime

class Imagenes(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'imagenes'
    _description = 'Imagenes de los animales'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'fecha desc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS
    
    imagen = fields.Image("Imagen", required=True)
    fecha = fields.Datetime("Fecha y hora de la revisión", required=True)
    animal = fields.Many2one('animales', store=True, required=True)

    # FUNCIONES
    
    # Función usada para comprobar que la fecha no es posterior a la actual
    @api.constrains('fecha')
    def comprobar_fecha_revision(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si la fecha del registro es posterior a la actual lanzaremos una excepción
            if record.fecha > datetime.now():
                raise models.ValidationError('La fecha de la imagen debe ser anterior a la actual')    