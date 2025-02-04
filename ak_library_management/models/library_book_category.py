# -*- coding: utf-8 -*-

from odoo import models, fields

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Category'
    _rec_name = 'name'

    # field's name
    name = fields.Char(string='Category Name', required=True)
    tag_ids = fields.Many2many('library.book.tags', string='Tags')

