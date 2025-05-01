# -*- coding: utf-8 -*-
{
    'name': 'Website Product Availability',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Custom out-of-stock page for website shop',
    'description': """
        This module adds out-of-stock functionality to the Odoo website shop
    """,
    'author': 'Pratham Shah',
    'website': 'https://www.aktivsoftware.com',
    'depends': ['website_sale', 'product'],
    'data': [
        'views/product_template_views.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}