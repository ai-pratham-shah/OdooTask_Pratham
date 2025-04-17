# -*- coding: utf-8 -*-
{
    'name': 'Shop Customisation',
    'version': '18.0.1.0.0',
    'author': 'Pratham shah',
    'summary': 'Shop Customisation Module',
    'description': "Shop Customisation",
    'website': 'https://www.aktivsoftware.com',
    'depends':['sale_management','website','website_sale','stock','contacts'],
    'data': [
        'views/add_to_cart.xml',
    ],
    'assets': {
        'web.assets_frontend': [
           'pratham_shop_customisation/static/src/js/add_to_cart.js'
        ]
    },
    'application': True,
    'license': 'LGPL-3',
}