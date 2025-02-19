# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BulkUploadBooks(models.TransientModel):
    _name = 'bulk.upload.books'
    _description = 'Bulk upload books'

    #fields
    book_names = fields.Text(string='Book Names', required=True,
                             help='Comma-separated list of book names')
    author_id = fields.Many2one(comodel_name='res.partner', string='Author')
    product_count = fields.Integer(string="Product Count", compute="_compute_product_count", default=0)

    @api.depends('book_names')
    def _compute_product_count(self):
        """ Computes the count of created products dynamically """
        # single_book = self.book_names.split(',')
        # product = self.env["product.template"].search([("name", "=", book)])
        # for book in single_book:
        #     if product:
        #         self.product_count += 1
        #     elif self.product_count != 0:
        #         self.product_count -= 1
        #     else:
        #         self.product_count = 0
   
        single_book = self.book_names.split(',')

        # Search all products at once to avoid multiple database hits
        products = self.env["product.template"].search([("name", "in", single_book)])

        # Convert the result into a set of product names for faster lookup
        existing_books = {product.name for product in products}

        # Calculate product count using a one-liner
        self.product_count = sum(
            1 for book in single_book if book in existing_books) if self.product_count != 0 else 0

    def create_product(self):
        """
        To create a bulk product
        """
        single_book = self.book_names.split(',')
        existing_products = self.env['product.template'].search([('name', 'in', single_book)])
        for book_name in single_book:
            book_name = book_name.strip()
            if not existing_products:
                self.env['product.template'].create({
                        'name': book_name,
                        'author': self.author_id.name,
                    })

    def revert_changes(self):
        """
        To delete the current product from product template
        """
        single_book = self.book_names.split(',')
        self.env["product.template"].search([("name", "=", single_book)]).unlink()

    def get_product(self):
        """ To get the form view and list based on some conditions """
        domain = [('name', 'in', self.book_names.split(','))]
        # Search for the products based on the domain
        products = self.env['product.template'].search(domain)
        # If only one product, open the product form view; otherwise, open product list
        action = {
            'name': 'Created Products' if len(products) > 1 else 'Product Form',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form' if len(products) > 1 else 'form',
            'domain': domain if len(products) > 1 else [],
            'res_id': products[0].id if len(products) == 1 else None, # Open the form of the first product if only one
        }
        return action
