# -*- coding: utf-8 -*-
{
    'name': "IT Base",    
    'version': '1.0.1',
    'author': "Marco Gonzalez",
    'category': "Tools",
    'summary': "Inventario, asignaciones de equipos de computo",
    'description': "Control de Equipos de computo",
    'website': "http://www.yourcompany.com",
    'depends': [],
    'data': [
        'data/itbase.data.xml',
        'security/ir.model.access.csv',
        'views/itbase_computadora.xml',
        'views/itbase_mantenimiento.xml',
        'views/itbase_carta_responsiva.xml',
        'views/itbase_soluciones.xml',
        'views/itbase_soporte.xml',
        'views/itbase_soporte_template.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'depends': ['mail'],
    'installable': True,
}