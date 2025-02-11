# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BulkUploadBooks(models.TransientModel):
    _name = 'bulk.upload.books'
    _description = 'Bulk upload books'
    _rec_name = "book_names"

    book_names = fields.Text(string='Book Names', required=True, help='Comma-separated list of book names')
    author = fields.Many2one(comodel_name='res.partner',string='Author')

    def create_product(self):
        book_names = self.book_names.split(',')
        existing_products = self.env['product.template'].search([('name', 'in', book_names)])
        existing_product_names = existing_products.mapped('name')
        for book_name in book_names:
            book_name = book_name.strip()  # Strip whitespace around book name
            if book_name and book_name not in existing_product_names:
                self.env['product.template'].create({
                    'name': book_name,
                    'author': self.author.name
                })

    def revert_changes(self):
        pass

    def get_product_count(self):
        pass