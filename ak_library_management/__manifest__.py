# -*- coding: utf-8 -*-
{
    'name': 'library management',
    'version': '18.0.1.0.0',
    'author' : 'Pratham shah',
    'summary': 'Library management module',
    'description': """
        Module that is designed to manage all the functions of a library 
        """,
    'category': 'Library_management/Library_management',
    'website': 'https://www.aktivsoftware.com',
    'depends': [
        'stock', 'web', 'sale_management','base_automation','hr'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'reports/library_location_report_action.xml',
        'reports/library_location_report.xml',
        'views/library_book.xml',
        'views/library_member.xml',
        'views/library_book_tag.xml',
        'views/library_book_category.xml',
        'views/library_book_location.xml',
        'views/product_template_view.xml',
        'views/product_variant_menu.xml',
        'views/res_user.xml',
        'views/sale_order.xml',
        'views/borrow_transaction_history.xml',
        'views/res_partner.xml',
        'views/stock_warehouse.xml',
        'views/res_config_setting.xml',
        'wizard/bulk_book.xml',
        'wizard/sale_order_wizard.xml',
        'wizard/borrow_books_warning_wizard.xml',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
