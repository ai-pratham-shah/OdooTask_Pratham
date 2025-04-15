# -*- coding: utf-8 -*-

from odoo import models, fields,api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.model
    def create(self, vals):
        """
        Override create to enforce vendor assignment logic
        """
        product_tmpl_id = vals.get('product_tmpl_id')
        product_id = vals.get('product_id')

        if product_tmpl_id and product_id:
            product_tmpl = self.env['product.template'].browse(product_tmpl_id)
            product = self.env['product.product'].browse(product_id)

            # Validate vendor assignment follows template settings
            if product_tmpl.vendor_on_variants and product.product_tmpl_id.id == product_tmpl_id:
                # When template enforces vendors, don't allow variant-specific ones
                vals['product_id'] = False
            elif not product_tmpl.vendor_on_variants and product.product_tmpl_id.id == product_tmpl_id:
                # When template doesn't enforce vendors, make it variant-specific
                vals['product_tmpl_id'] = False

        return super(ProductSupplierinfo, self).create(vals)

    def write(self, vals):
        result = super(ProductSupplierinfo, self).write(vals)

        # After updating vendor records, check if we need to sync with variants
        templates_to_sync = self.env['product.template']
        for record in self:
            if not record.product_id and record.product_tmpl_id.vendor_on_variants:
                # This is a template-level vendor and vendor_on_variants is True
                templates_to_sync |= record.product_tmpl_id

        # Sync template vendors to variants for affected templates
        for template in templates_to_sync:
            template._sync_template_vendors_to_variants()