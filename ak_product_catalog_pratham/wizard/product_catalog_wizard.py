# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ProductCatalogWizard(models.TransientModel):
    _name = 'product.catalog.wizard'
    _description = 'Product Catalog Generator Wizard'

    catalog_style = fields.Selection([
        ('style1', 'Style 1'),
        ('style2', 'Style 2')
    ], string='Catalog Style', required=True, default='style1')

    page_break_after = fields.Integer(string='Page Break After', default=5, required=True,
                                      help='Number of products before a page break')

    product_ids = fields.Many2many('product.product', string='Products', required=True)

    @api.constrains('page_break_after')
    def _check_page_break_after(self):
        for wizard in self:
            if not (0 < wizard.page_break_after <= 5):
                raise UserError("Page Break After must be between 1 and 5")

    def action_generate_catalog(self):
        self.ensure_one()
        # Select the appropriate report based on the style
        if self.catalog_style == 'style1':
            report_name = 'ak_product_catalog_pratham.report_product_catalog_style1_action'
        else:
            report_name = 'ak_product_catalog_pratham.report_product_catalog_style2'

        # Return the PDF report action
        return self.env.ref(report_name).report_action(self)
