# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Usuarios(models.Model):
    # NOMBRE Y DESCRIPCIÓN DEL MODELO
    _name = 'usuarios'
    _description = 'Usuarios de la protectora'


    # PARÁMETROS DE ORDENACIÓN POR DEFECTO
    _order = 'rol asc, usuario asc'


    # Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    # se necesite un nombre, se usara el atributo usuario
    _rec_name = 'usuario'    

    # VARIABLES QUE USAREMOS EN LOS CAMPOS SELECTION

    # Roles que pueden adoptar los usuarios
    ROLES = [
        ('voluntario', 'Voluntario'),
        ('adoptante', 'Adoptante'),
    ]


    # ATRIBUTOS

    usuario = fields.Char("Usuario", required=True)
    nombreCompleto = fields.Char("Nombre completo", required=True)
    rol = fields.Selection(ROLES, default=ROLES[0][0], required=True)
    email = fields.Char("Email", required=True)
    contrasenya = fields.Char("Contraseña", required=True)
    telefono = fields.Char("Teléfono")
    direccion = fields.Char("Dirección")
    ciudad = fields.Char("Ciudad")
    codigoPostal = fields.Char("Código postal")
    permisoPPP = fields.Boolean("Permiso de perro potencialmente peligroso")
    foto = fields.Image("Foto")
    observaciones = fields.Html('Observaciones', sanitize=True, strip_style=False)
    horario = fields.Char("Horario")
    fechaNacimiento = fields.Date("Fecha de nacimiento")
    edad = fields.Integer("Edad", compute="calcular_edad", store=False)
    token = fields.Char("Token")
    tokenCaducidad = fields.Date("Fecha de caducidad del token")

    # FUNCIONES

    # Función usada para calcular la edad en base a la fecha de nacimiento del usuario
    @api.depends('fechaNacimiento')
    def calcular_edad(self):
        today = date.today()
        for record in self:
            record.edad = today.year - record.fechaNacimiento.year - ((today.month, today.day) 
            < (record.fechaNacimiento.month, record.fechaNacimiento.day))

    # Constraints de SQL del modelo
    _sql_constraints = [
        ('usuario_uniq', 'UNIQUE (usuario)', 'El usuario introducido ya existe.'),
        ('email_uniq', 'UNIQUE (email)', 'El email introducido ya existe.')
    ]