# -*- coding: utf-8 -*-
{
    'name': "Protectora",  # Titulo del módulo
    'summary': "Módulo para protectoras de animales",  # Resumen de la funcionaliadad
    'description': """
    Módulo destinado a protectoras de animales, donde podrán manejar todos los datos relacionados con estos,
    los diferentes usuarios de la aplicación móvil y las diferentes entradas del blog.
    ==============
    """,  

    #Indicamos que es una aplicación
    'application': True,
    'author': "Federico Adria",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],

    'data': [      
        # Fichero que contendrá las directivas de acceso a los diferentes recursos
        'security/ir.model.access.csv',

        #Aqui distintas vistas de equipo (vistas diferentes, mismo modelo)
        'views/animales.xml',
        'views/usuarios.xml',
        'views/imagenes.xml',
        'views/revisiones.xml',
        'views/publicaciones.xml',
        'views/adopciones.xml',
        'views/graficos.xml',
        'views/requisitos.xml'
    ],
    # Fichero con data de demo si se inicializa la base de datos con "demo data" (No incluido en ejemplo)
    # 'demo': [
    #     'demo.xml'
    # ],
}
