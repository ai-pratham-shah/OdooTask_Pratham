{
    'name': 'Product Catalog PDF Generator',
    'version': '18.0.1.0.0',
    'author': 'Pratham shah',
    'summary': 'Generate customized PDF product catalogs',
    'description': """
        Product Catalog PDF Generator
        ============================
        This module adds a wizard to generate customized product catalogs in PDF format
        with different styles and layouts.
    """,
    'website': 'https://www.aktivsoftware.com',
    'depends': ['sale', 'product', 'stock','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'wizard/product_catalog_wizard.xml',
        'reports/report_product_catalog.xml',
        'reports/report_style1.xml',
        'reports/report_style2.xml',
    ],
    # 'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    # 'auto_install': False,
    'license': 'LGPL-3',
}