# -*- coding: utf-8 -*-

from odoo import models, fields,api
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
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved')
    ], 'Status', default='available', tracking=True)
    reference = fields.Char(readonly=True)

    @api.model_create_multi
    def create(self, vals):
        """
        This method is overriding reference filed with sequence number
        """
        res = super().create(vals)
        res.default_code = self.env['ir.sequence'].next_by_code('product.template')
        print('This is default_code:',res.default_code)
        return res

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

    def action_borrow_books(self):
        """Open the borrow books wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }