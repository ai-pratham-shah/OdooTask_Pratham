# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_seller_ids = fields.One2many(
        'product.supplierinfo',
        'product_id',
        string='Variant Vendors',
        help="List of vendors specific to this product variant"
    )

    def _prepare_sellers(self, params=False):
        """
        Override to consider variant-specific vendors
        Returns vendors list considering both variant and template levels
        """
        sellers = self.variant_seller_ids

        # If no variant-specific vendors and template allows inheritance
        if not sellers and self.product_tmpl_id.vendor_on_variants:
            # Use template vendors as fallback
            return self.product_tmpl_id.seller_ids

        return sellers