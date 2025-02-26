# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BulkUploadBooks(models.TransientModel):
    """
    This model facilitates the bulk upload of books as products.

    The user can enter a comma-separated list of book names, and
    the system will allow the creation of new product entries for
    each book name. The model also provides functionality for:
    - Checking the count of products created based on the book names.
    - Reverting the created products if needed.
    - Providing a mechanism to view and access the created products
      through smart buttons and actions.
    """
    _name = 'bulk.upload.books'
    _description = 'Bulk upload books'
    _rec_name = 'book_names'

    #fields
    book_names = fields.Text('Book Names', required=True,
                              help='Comma-separated list of book names')
    author_id = fields.Many2one('res.partner', 'Author', required=True)
    product_count = fields.Integer("Product Count",
                                   compute="_compute_product_count", default=0)

    @api.depends('book_names')
    def _compute_product_count(self):
        """
        It checks if a product already exists for each book name
        and calculates the count of such products.This count is used
        to display how many of the books in the `book_names` field already have
        corresponding products in the system.
        """
        single_book = self.book_names.split(',')
        self.product_count = sum(
            1 for book in single_book if self.env["product.template"].search([("name", "=", book)]))

    def create_product(self):
        """
        Creates new products based on the provided book names in the `book_names` field.
        It splits the book names from the comma-separated string, checks for
        existing products with the same name,and creates a new product if no
        existing product matches the book name.
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

                self.env['bus.bus']._sendone(
                    self.env.user.partner_id, 'simple_notification', {
                        'type': 'success',
                        'message': f"{book_name} is created.",
                    })

    def revert_changes(self):
        """
        Deletes the products created from the `book_names` field
        in the `product.template` model.It looks for products with
        names matching the provided `book_names` and removes them from
        the system.This method allows reverting the changes made by the
        `create_product` method, deleting the created products.
        """
        single_book = self.book_names.split(',')
        self.env["product.template"].search([("name", "=", single_book)]).unlink()
        for book_name in single_book:
            book_name = book_name.strip()
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"{book_name} is deleted.",
                })

    def get_product(self):
        """
        Returns an action to either show a list or form view of
        the products created based on the book names.It searches
        for products whose names match the ones in the `book_names` field and:
        - Opens a list view if multiple products are found.
        - Opens the form view of the first product if only one product is found.

        The action also ensures the correct domain and res_id are set based
        on the number of products found.
        """
        domain = [('name', 'in', self.book_names.split(','))]
        products = self.env['product.template'].search(domain)
        action = {
            'name': 'Created Products' if len(products) > 1 else 'Product Form',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form' if len(products) > 1 else 'form',
            'domain': domain if len(products) > 1 else [],
            'res_id': products[0].id if len(products) == 1 else None,
        }
        return action
