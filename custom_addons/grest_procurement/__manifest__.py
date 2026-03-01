# -*- coding: utf-8 -*-
{
    'name': 'GREST Procurement',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Device procurement tracking for GREST mobile refurbishment',
    'author': 'Raven Solutions',
    'website': 'https://godoo.sam9scloud.in',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/procurement_security.xml',
        'security/ir.model.access.csv',
        'views/procurement_views.xml',
        'views/procurement_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
