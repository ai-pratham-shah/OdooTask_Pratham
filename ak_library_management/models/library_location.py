# -*- coding: utf-8 -*-
from venv import create

from odoo import models,fields

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

