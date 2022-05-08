# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime

class Graficos(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'graficos'
    _description = 'Gráficos con los que poder visualizar diferentes datos'

    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'fecha desc'

    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS

    imagen = fields.Image("Imagen con el gráfico")
    titulo = fields.Char("Título del gráfico", required=True)
    fecha = fields.Datetime("Fecha y hora de publicación del gráfico", required=True)


    # FUNCIONES

    # Función usada para comprobar que la fecha no es posterior a la actual
    @api.constrains('fecha')
    def comprobar_fecha_publicacion(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si la fecha del registro es posterior a la actual lanzaremos una excepción
            if record.fecha > datetime.now():
                raise models.ValidationError('La fecha del gráfico debe ser anterior a la actual')