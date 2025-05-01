# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleOutOfStock(WebsiteSale):

    def sitemap_products(env, rule, qs):
        return super().sitemap_products(env, rule, qs)

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True,
           sitemap=sitemap_products, readonly=True)
    def product(self, product, category='', search='', **kwargs):
        if product.is_out_of_stock:
            return request.render('custom_out_of_stock_page.out_of_stock_page', {
                'product': product,
            })
        return super(WebsiteSaleOutOfStock, self).product(product, category=category, search=search, **kwargs)