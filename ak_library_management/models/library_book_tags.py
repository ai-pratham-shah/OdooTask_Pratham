# -*- coding: utf-8 -*-
from odoo import models,fields

class LibraryBookTags(models.Model):
    """
    The LibraryBookTags model is used to store detailed information about book tag in the library
    system.It includes information such as the Book Tag of the book.
    """
    _name = 'library.book.tags'
    _description = 'Book tag'

    # field's name
    name = fields.Char(string='Book tag', required=True)