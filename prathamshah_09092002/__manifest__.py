# -*- coding: utf-8 -*-

{
    'name': 'backend exam',
    'version': '18.0.1.0.0',
    'author' : 'Pratham shah',
    'description': """
        custom approval workflow on the Sales Order module
        """,
    'website': 'https://www.aktivsoftware.com',
    'depends': ['sale_management','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_manager_approval.xml',
        'views/res_config_setting.xml',
        'report/sale_order_report.xml',
        'views/sale_order.xml',
        'data/ir_cron.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}