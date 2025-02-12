# -*- coding: utf-8 -*-

from odoo import models, fields

class LibraryBookCategory(models.Model):
    """
    The LibraryBookCategory model is used to store detailed information about books categories and ids in the library
    system.It includes information such as the Category name, Tags of the book.
    """
    _name = 'library.book.category'
    _description = 'Book Category'

    # field's name
    name = fields.Char(string='Category Name', required=True)
    tag_ids = fields.Many2many('library.book.tags', string='Tags')