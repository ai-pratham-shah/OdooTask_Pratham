# -*- coding: utf-8 -*-
from pkg_resources import require

from odoo import models,fields

class LibraryBookTags(models.Model):
    _name = 'library.book.tags'
    _description = 'Book tag'
    _rec_name = 'name'

    # field's name
    name = fields.Char(string='Book tag', required=True)