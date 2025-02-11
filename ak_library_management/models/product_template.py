# -*- coding: utf-8 -*-

from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """
    Inherit product template model from addons and add some custom fields.
    """
    #fields
    is_library_book = fields.Boolean(string='Is library book')
    author = fields.Char(string='Author')
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    barcode = fields.Char(string='Isbn Number')
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved')
    ], string='Status', default='available', tracking=True)

    def action_mark_borrowed(self):
        """
        This method is created for marked book as borrowed
        and this method is used in button in xml side
        """
        self.status = 'borrowed'

    def action_mark_available(self):
        """
        This method is created for marked book as available
        and this method is used in button in xml side
        """
        self.status = 'available'





