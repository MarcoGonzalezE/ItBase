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
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
}