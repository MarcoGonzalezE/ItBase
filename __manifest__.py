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
        'data/website.menu.csv',
        'security/ir.model.access.csv',        
        'views/itbase_basedatos.xml',        
        'views/itbase_mantenimiento.xml',        
        'views/itbase_servidores.xml',
        'views/itbase_inventario.xml',
        'views/itbase_companias.xml',
        'views/itbase_carta_responsiva.xml',
        'views/itbase_soluciones.xml',
        'views/itbase_soporte.xml',
        'views/itbase_template.xml',
        'views/itbase_proyectos.xml',
        'views/itbase_departamento.xml',
        'views/itbase_reuniones.xml',
        'views/itbase_redes.xml',
        'views/itbase_configuracion.xml',
        'views/itbase_recordatorios.xml',
        'views/menu.xml',
        'wizard/itbase_wizard_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
    'depends': ['mail','web', 'website'],
    'installable': True,
}