from odoo import models, fields

class BorrowBooksWarningWizard(models.TransientModel):
    _name = 'borrow.books.warning.wizard'
    _description = 'Borrow Books Warning Wizard'

    message = fields.Text(string="Warning Message", readonly=True)

