# -*- coding: utf-8 -*-
from odoo import models,fields,api


class LibraryBookLocation(models.Model):
    """
    The LibraryBookLocation model is used to store detailed information
    about book location in the library system.It includes information
    such as the Book name, Location, Capacity, Notes,Books of the book.
    """
    _name = 'library.book.location'
    _description = 'Book Location'
    _inherit = ['mail.thread']

    # field's name
    name = fields.Char(string='Library Name', tracking=True)
    location = fields.Char(string='Location', tracking=True)
    capacity = fields.Integer(string='Capacity')
    librarian_id = fields.Many2one('res.users',
                                string="Librarian",
                                tracking=True)
    notes = fields.Char(string='Notes')
    book_ids = fields.Many2many('product.template',
                                domain=[('is_library_book', '=', True)] ,
                                string='Books')
    borrowed_books_count = fields.Integer("Borrowed Books Count",
                                          compute='_compute_borrowed_books',
                                          store=False)
    _sql_constraints = [('name_uniq', "unique(name)", "Library name already exists.")]

    @api.depends('book_ids')
    def _compute_borrowed_books(self):
        """
        This compute method is created for to count only borrowed books from library
        """
        for record in self:
            record.borrowed_books_count = (
                self.env['product.template'].search_count([('status', '=', 'borrowed'),
                                                           ('id', 'in', record.book_ids.ids)
]))

    def action_view_borrowed_books(self):
        """
        With the help of this function we can show or list only borrowed books
        """
        return {
            'name': 'Borrowed Books',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.template',
            'domain': [('status', '=', 'borrowed'),('id','in',self.book_ids.ids)],
            'context': {'default_is_library_book': True},
        }

    @api.constrains('book_ids')
    def _check_book_ids(self):
        """
        This function send notification to librarian
        whenever book is delete or add in M2M field
        """
        self.env['bus.bus']._sendone(self.librarian_id.partner_id, 'simple_notification', {
            'type': 'success',
            'message': f"In library[{self.name}] books list updated.",
        })