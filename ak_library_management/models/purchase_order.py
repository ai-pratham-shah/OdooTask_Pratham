# -*- coding: utf-8 -*-

from odoo import models, fields,api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, supplier, po):
        """
        Override to use variant-specific vendor information when available
        """
        res = super(PurchaseOrder, self)._prepare_purchase_order_line(
            product_id, product_qty, product_uom, company_id, supplier, po)

        # Check if this is a variant with its own supplier info
        if product_id and not product_id.product_tmpl_id.vendor_on_variants:
            # Use variant-specific vendor if available
            seller = product_id.variant_seller_ids.filtered(
                lambda s: s.name == supplier.name and
                          (not s.company_id or s.company_id == company_id)
            )

            if seller:
                # Update price and other vendor-specific details
                if seller and res.get('price_unit'):
                    res['price_unit'] = seller[0].price

                if seller and res.get('date_planned'):
                    res['date_planned'] = self._get_date_planned(seller[0], po=po)

        return res