
"""
  @Author: Federico Adrià Carrasco
  @Date: 04/06/2022
  @Email: fadriacarrasco@gmail.com
"""

# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime

class Adopciones(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'adopciones'
    _description = 'Adopciones de la protectora'

    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'vigente desc, fecha desc'

    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo id
    _rec_name = 'id'    

    # ATRIBUTOS

    fecha = fields.Datetime("Fecha y hora de la adopción", required=True)
    animal = fields.Many2one('animales', store=True, required=True)
    dueño = fields.Many2one('usuarios', store=True, required=True)
    vigente = fields.Boolean("Adopción vigente")

    # FUNCIONES

    # Función usada para marcar un animal como adoptado, o no, según la vigencia de la adopción
    @api.onchange('vigente')
    def comprobar_adopcion_animal(self):
        # Bucle donde obtendremos el valor del registro creado y/o actualizado
        for record in self:
            # Bucle donde comprobaremos si este animal tiene una adopción vigente
            for adopcion in self.env['adopciones'].search([]):
                # Nos saltaremos el nuevo registro, este no será comparado consigo mismo
                if record.id != adopcion.id:
                    if record.vigente == True and adopcion.vigente == True and adopcion.animal == record.animal:
                        # Este animal ya está adoptado, no podremos tener otra adopción vigente
                        raise models.ValidationError('Error: el animal ya se encuentra adoptado.')

            # Si no tiene adopciones vigentes, actuaremos según el valor del nuevo registro y/o actualización
            if record.vigente == True:
                record.animal.adoptado = True
            else:
                record.animal.adoptado = False

    # Función usada para comprobar que no se introduce una fecha posterior a la actual
    @api.constrains('fecha')
    def comprobar_fecha_adopcion(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:
            # Comprobamos que la fecha no es posterior a la actual, si lo es lanzaríamos un error
            if record.fecha > datetime.now():
                raise models.ValidationError('La fecha de adopción debe ser anterior a la actual')

    # Función usada para comprobar que un PPP sólo puede ser adoptado por una persona que disponga del permiso necesario
    @api.onchange('dueño')
    def comprobar_permiso_ppp(self):
        # Bucle donde comprobaremos si el animal puede ser adoptado por este usuario
        for record in self:
            # Comprobamos que se trata de un animal peligroso y que el dueño disponga del permiso necesario
            if record.animal.perroPeligroso is True and record.dueño.permisoPPP is not True:
                raise models.ValidationError('El usuario introducido no puede adoptar perros potencialmente peligrosos')

    # Función usada para impedir eliminar adopciones vigentes
    def unlink(self):
        if self.vigente == True:
            raise models.ValidationError('No es posible eliminar una adopción vigente')
        return super(Adopciones, self).unlink()