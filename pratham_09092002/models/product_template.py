# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """
    Inherit product template model from addons and add some custom fields.
    """
    #fields
    product_review_ids = fields.One2many('product.review', 'product_id',
                                         string='Product Reviews')
