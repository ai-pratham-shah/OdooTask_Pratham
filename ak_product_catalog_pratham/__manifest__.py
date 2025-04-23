{
    'name': 'Product Catalog PDF Generator',
    'version': '18.0.1.0.0',
    'author': 'Pratham shah',
    'summary': 'Generate customized PDF product catalogs',
    'description': """
        Product Catalog PDF Generator
        """,
    'website': 'https://www.aktivsoftware.com',
    'depends': ['base', 'sale', 'product', 'stock', 'sale_management','spreadsheet_edition'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_catalog_wizard.xml',
        'views/menu_view.xml',
        'reports/report_product_catalog_style1_document.xml',
        'reports/report_product_catalog_style2_document.xml',
        'reports/report_product_catalog.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
