{
    'name': 'User Onboarding Process',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Custom onboarding process for new users',
    'description': """
        User Onboarding Process
    """,
    'author': 'Pratham Shah',
    'website': 'https://www.example.com',
    'depends': ['base', 'web', 'mail', 'portal', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        'views/onboarding_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'pratham_frontend_document2/static/src/css/onboarding.css',
            'pratham_frontend_document2/static/src/js/onboarding.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}