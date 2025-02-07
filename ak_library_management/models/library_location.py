# -*- coding: utf-8 -*-
from odoo import models,fields,api

class LibraryBookLocation(models.Model):
    _name = 'library.book.location'
    _description = 'Book Location'
    _rec_name = 'name'

    # field's name
    name = fields.Char(string='Book Name')
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    notes = fields.Char(string='Notes')
    book_ids = fields.Many2many(comodel_name='product.template',domain=[('is_library_book', '=', True)] ,string='Books')
    borrowed_books_count = fields.Integer(string="Borrowed Books Count", compute='_compute_borrowed_books')

    @api.depends('book_ids')
    def _compute_borrowed_books(self):
        """
        This compute method is created for to count only borrowed books from library
        """
        for record in self:
            record.borrowed_books_count = self.env['product.template'].search_count([('status', '=', 'borrowed')])

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
        }
