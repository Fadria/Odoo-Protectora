
"""
  @Author: Federico Adrià Carrasco
  @Date: 04/06/2022
  @Email: fadriacarrasco@gmail.com
"""

# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Animales(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'animales'
    _description = 'Animales de la protectora'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'adoptado asc, urgente desc, nombre asc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo nombre
    _rec_name = 'nombre'    


    # VARIABLES QUE USAREMOS EN LOS CAMPOS SELECTION

    # Especies de los animales

    ESPECIES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('huron', 'Hurón'),
        ('fenec', 'Fénec'),
        ('ajolote', 'Ajolote'),
        ('guacamayo', 'Guacamayo')
    ]

    # Sexo de los animales
    SEXO = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
        ('desconocido', 'Desconocido'),
    ]

    # Tamaño de los animales
    TAMANYO = [
        ('pequenyo', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]


    # ATRIBUTOS

    nombre = fields.Char("Nombre", required=True)
    imagen = fields.Image("Imagen")
    chip =  fields.Boolean("Chip")
    especie = fields.Selection(ESPECIES, default=ESPECIES[0][0], required=True)
    raza = fields.Char("Raza")
    nacimiento = fields.Date("Fecha de nacimiento", required=True)
    edad = fields.Integer("Edad", compute="calcular_edad", store=False)
    sexo = fields.Selection(SEXO, default=SEXO[0][0], required=True)
    tamanyo = fields.Selection(TAMANYO, default=TAMANYO[0][0], required=True)
    adoptado = fields.Boolean("Adoptado")
    urgente = fields.Boolean("Urgente")
    peso = fields.Float("Peso")
    esterilizado = fields.Boolean("Esterilizado")
    exotico = fields.Boolean("Animal exótico")
    observaciones = fields.Text('Observaciones')
    pelo = fields.Boolean("¿Tiene pelo?")
    historia = fields.Text('Historia del animal')
    perroPeligroso = fields.Boolean("Perro potencialmente peligroso")
    imagenes = fields.One2many("imagenes", "animal")
    revisiones = fields.One2many("revisiones", "animal")

    # FUNCIONES

    # Función usada para calcular la edad en base a la fecha de nacimiento del animal
    @api.depends('nacimiento')
    def calcular_edad(self):
        today = date.today()
        for record in self:
            record.edad = today.year - record.nacimiento.year - ((today.month, today.day) 
            < (record.nacimiento.month, record.nacimiento.day))