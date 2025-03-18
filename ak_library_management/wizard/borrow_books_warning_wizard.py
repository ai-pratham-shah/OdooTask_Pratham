# -*- coding: utf-8 -*-
from odoo import models, fields


class BorrowBooksWarningWizard(models.TransientModel):
    _name = 'borrow.books.warning.wizard'
    _description = 'Borrow Books Warning Wizard'

    borrow_wizard_id = fields.Many2one(comodel_name='borrow.transaction.history', string="Borrow Transaction")
    message = fields.Text(string="Warning Message", readonly=True)
    next_action = fields.Text(string="Next Warning", readonly=True)

    def action_continue(self):
        """ Handles the 'Continue' button:
        - If more warnings exist, display them sequentially.
        - If no more warnings, finalize the borrow transaction.
        """
        next_warnings = eval(self.next_action) if self.next_action else []
        if next_warnings:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warning',
                'res_model': 'borrow.books.warning.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_borrow_wizard_id': self.borrow_wizard_id.id,
                    'default_message': next_warnings[0],
                    'default_next_action': repr(next_warnings[1:]) if len(next_warnings) > 1 else None
                }
            }
        else:
            # No more warnings, proceed with the transaction
            return self.borrow_wizard_id._process_borrow_transaction()

    def action_cancel(self):
        """ If 'Cancel' is clicked, delete the transaction. """
        self.borrow_wizard_id.unlink()
        return {'type': 'ir.actions.act_window_close'}
