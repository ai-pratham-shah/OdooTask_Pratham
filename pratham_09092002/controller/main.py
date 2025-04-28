# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ProductReviewController(http.Controller):

    @http.route(['/shop/product/submit_review'], type='http', methods=['POST'], auth="user", website=True)
    def submit_review(self, **post):
        """Handle the submission of a product review"""
        if not post.get('product_id') or not post.get('rating') or not post.get('description'):
            return request.redirect('/shop')
        vals = {
            'product_id': int(post.get('product_id')),
            'rating': post.get('rating'),
            'description': post.get('description'),
        }
        request.env['product.review'].sudo().create(vals)
        return request.render('pratham_09092002.review_success_template')
