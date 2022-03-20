# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Animales(models.Model):
    # Nombre y descripcion del modelo
    _name = 'animales'
    _description = 'Animales de la protectora'

    # Parametros de ordenacion por defecto
    _order = 'nombre'

    # ATRIBUTOS

    # PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR NOMBRE DE UN REGISTRO
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
    # Indicamos que atributo sera el que se usara para mostrar nombre.
    # Por defecto es "name", pero si no hay un atributo que se llama name, aqui lo indicamos
    # Aqui indicamos que se use el atributo "nombre"
    _rec_name = 'nombre'    

    # Variable de donde obtendremos las especies de los animales
    ESPECIES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('pajaro', 'Pájaro'),
        ('huron', 'Hurón')
    ]

    # Variable de donde obtendremos el sexo de los animales
    SEXO = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
        ('desconocido', 'Desconocido'),
    ]

    # Variable de donde obtendremos el tamaño de los animales
    TAMANYO = [
        ('pequenyo', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]

    # Elementos de cada fila del modelo de datos
    # Los tipos de datos a usar en el ORM son 
    # https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html#fields

    nombre = fields.Char("Nombre", required=True)
    chip =  fields.Boolean("Chip")
    especie = fields.Selection(ESPECIES, default=ESPECIES[0][0])
    raza = fields.Char("Raza")
    nacimiento = fields.Date("Fecha de nacimiento", required=True)
    edad = fields.Integer("Edad", compute="calcular_edad", store=False)
    sexo = fields.Selection(SEXO, default=SEXO[0][0])
    tamanyo = fields.Selection(TAMANYO, default=TAMANYO[0][0])
    urgente = fields.Boolean("Urgente")
    peso = fields.Float("Peso")
    esterilizado = fields.Boolean("Esterilizado")
    exotico = fields.Boolean("Animal exótico")
    observaciones = fields.Html('Observaciones', sanitize=True, strip_style=False)
    pelo = fields.Boolean("¿Tiene pelo?")
    historia = fields.Html('Historia del animal', sanitize=True, strip_style=False)
    permisoEspecial = fields.Boolean("¿Necesita un permiso especial?")

    @api.depends('nacimiento')
    def calcular_edad(self):
        today = date.today()
        for record in self:
            record.edad = today.year - record.nacimiento.year - ((today.month, today.day) 
            < (record.nacimiento.month, record.nacimiento.day))