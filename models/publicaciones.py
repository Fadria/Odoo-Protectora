
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
    contenido = fields.Text('Contenido', required=True)
    autor = fields.Many2one("usuarios", "Autor", required=True) # Relación con el modelo de usuarios
    imagenPie = fields.Image("Imagen en el pie")

    # FUNCIONES

    # Función usada para comprobar que la fecha no es posterior a la actual
    @api.constrains('fechaPublicacion')
    def comprobar_fecha_publicacion(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si la fecha del registro es posterior a la actual lanzaremos una excepción
            if record.fechaPublicacion > datetime.now():
                raise models.ValidationError('La fecha de publicación debe ser anterior a la actual')

    # Función usada para comprobar que en el campo autor se ha asignado una persona con el rol voluntario
    @api.constrains('autor')
    def comprobar_autor(self):
        # Bucle donde comprobaremos si el nuevo registro es correcto
        for record in self:

            # Si el usuario no es un voluntario lanzaremos una excepción
            if record.autor.rol != "voluntario":
                raise models.ValidationError('La persona que realiza la revisión debe ser un voluntario')