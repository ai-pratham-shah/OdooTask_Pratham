# -*- coding: utf-8 -*-
from odoo import models, fields


class BorrowBooksWarningWizard(models.TransientModel):
    _name = 'borrow.books.warning.wizard'
    _description = 'Borrow Books Warning Wizard'

    message = fields.Text(string="Warning Message", readonly=True)

    def action_cancel(self):
        """
        To delete current record
        """
        record_id = self.env.context.get('active_id')
        self.env["borrow.transaction.history"].browse(record_id).unlink()