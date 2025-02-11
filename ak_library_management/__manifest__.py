# -*- coding: utf-8 -*-

{
    'name': 'Ak library management',
    'version': '18.0.1.0.0',
    'author' : 'Pratham shah',
    'summary': 'Library management module',
    'description': """
        Module that is designed to manage all the functions of a library 
        """,
    'category': 'Library_management/Library_management',
    'website': 'https://www.aktivsoftware.com',
    'depends': [
        'product', 'web', 'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_member.xml',
        'views/library_book_tag.xml',
        'views/library_book_category.xml',
        'views/library_book_location.xml',
        'views/product_template_view.xml',
        'views/product_template_barcode_view.xml',
        'views/product_variant_menu.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
