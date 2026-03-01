# -*- coding: utf-8 -*-
{
    'name': 'GREST Accounts Approval',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Accounts approval workflow for GREST device procurement',
    'author': 'Raven Solutions',
    'website': 'https://godoo.sam9scloud.in',
    'depends': ['base', 'grest_procurement'],
    'data': [
        'security/accounts_security.xml',
        'security/ir.model.access.csv',
        'views/accounts_approval_views.xml',
        'views/accounts_approval_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
