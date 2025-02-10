# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryBook(models.Model):
    """
    The LibraryBook model is used to store detailed information about books in the library system.
    It includes information such as the title, author, ISBN number, publication date, category,
    tags, availability status, description, and location of the book.
    """
    _name = "library.book"
    _description = "Stores book-related details"
    _rec_name = "name"

    # field's name
    name = fields.Char(string='Book Title', required=True)
    author = fields.Char(string='Author Name')
    isbn = fields.Char(string='ISBN Number')
    publication_date = fields.Date(string='Date of Publication')
    category_id = fields.Many2one(comodel_name='library.book.category',string='Book category')
    tags_ids = fields.Many2many(comodel_name='library.book.tags',
                                string='Tags', related='category_id.tag_ids')
    state = fields.Selection([('available', 'Available'), ('borrowed', 'Borrowed')],
                             string='Book Availability')
    description = fields.Text(string='BookSummary')
    library_id = fields.Many2one('library.book.location', string='Book Location')

