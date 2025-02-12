# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BulkUploadBooks(models.TransientModel):
    _name = 'bulk.upload.books'
    _description = 'Bulk upload books'
    _rec_name = "book_names"

    #fields
    book_names = fields.Text(string='Book Names', required=True,
                             help='Comma-separated list of book names', default="")
    author = fields.Many2one(comodel_name='res.partner', string='Author')
    check = fields.Boolean("check", default=False)
    product_count = fields.Integer(string="Product Count", compute="_compute_product_count")

    @api.depends('book_names')
    def _compute_product_count(self):
        """ Computes the count of created products dynamically """
        if self.check:
            self.product_count = len(self.book_names.split(','))
        elif self.check == False and self.product_count != 0:
            self.product_count -= len(self.book_names.split(','))
        else:
            self.product_count = 0

    def create_product(self):
        """
        To create a bulk product
        """
        book_names = self.book_names.split(',')
        existing_products = self.env['product.template'].search([('name', 'in', book_names)])
        existing_product_names = existing_products.mapped('name')
        created_products = []
        for book_name in book_names:
            book_name = book_name.strip()
            if book_name and book_name not in existing_product_names:
                product = (self.env['product.template'].create
                    ({
                        'name': book_name,
                        'author': self.author.name,
                    }))
                created_products.append(product.ids)
        self.check = True

    def revert_changes(self):
        """
        To delete the current product from product template
        """
        single_book = self.book_names.split(',')
        for book in single_book:
            existing_record = self.env["product.template"].search([("name", "=", book)])
            existing_record.unlink()
        self.check = False

    def get_product_count(self):
        """ To get the product count """
        domain = [('name', 'in', self.book_names.split(','))]
        if self.product_count == 1:
            product = self.env['product.template'].search(domain, limit=1)  # Get the single product
            return {
                'name': 'Product Form',
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': product.id,  # Directly open the form of this product
            }
        return {
            'name': 'Created Products',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': domain,
        }
