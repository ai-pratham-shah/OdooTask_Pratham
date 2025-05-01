# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """
    Add two custom field under the inventory page.
    """

    is_out_of_stock = fields.Boolean(
        string="Not Available (Out of Stock)",
        default=False,
        help="Check this if the product is currently out of stock"
    )

    out_of_stock_message = fields.Html(
        string="Custom Out-of-Stock Message",
        help="Custom message to display when the product is out of stock"
    )