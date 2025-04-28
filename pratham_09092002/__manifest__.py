{
    'name': 'frontend exam',
    'version': '18.0.1.0.0',
    'author' : 'Pratham shah',
    'description': """
        Enhance the product page on the Odoo website to
        allow logged-in users to rate products and submit reviews.
        """,
    'website': 'https://www.aktivsoftware.com',
    'depends': ['website','website_sale','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_review_views.xml',
        'views/product_template_views.xml',
        'views/main.xml',
    ],
    'assets' : {
        'web.assets_frontend': [
            'product_review/static/src/js/product_review.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}