# -*- coding: utf-8 -*-
{
    'name': 'Gov_tax_manager',
    'version': '16.0',
    'summary': """ Gov_tax_manager Summary """,
    'author': 'Isaachintosh / AosDevs',
    'website': 'https://www.odoocast.com.br',
    'category': 'account',
    'depends': ['base', 'account'],
    "data": [
        "security/ir.model.access.csv",
        "views/gov_tax_rate_views.xml",
        "views/gov_tax_rate_line_views.xml",
        "views/gov_tax_guide_views.xml",
        "views/res_partner_property_views.xml"
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
