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
        ('reserved', 'Reserved'),
        ('unavailable','Unavailable')
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

    def _compute_display_name(self):
        """
        override compute display name and change book name format to
        [author_name]book_name.
        """
        for record in self:
            # Use f-string for better readability and performance
            if self._context.get('add_author') and record.author:
                record.display_name = f"[{record.author}] {record.name}"
            else:
                record.display_name = record.name
    @api.model
    @api.readonly
    def name_search(self, name='', args=None, operator='ilike', limit=None):
        """Override name_search method to search book by author name."""
        # Ensure 'args' is a list if it is None
        args = args or []
        if name:
            # Add condition to search by author
            args.append(('author', operator, name))

        # Call the parent method with updated arguments
        return super().name_search(name='', args=args, operator=operator, limit=limit)
    def action_borrow_books(self):
        """Open the borrow books wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }

