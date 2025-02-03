# -*- coding: utf-8 -*-

from odoo import models,fields

class LibraryBookLocation(models.Model):
    _name = 'library.book.location'
    _description = 'Book Location'

    name = fields.Char(string='Book Name')
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    notes = fields.Char(string='Notes')
    book_ids = fields.One2many('library.book', 'library_id', string='Books')

