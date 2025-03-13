# -*- coding: utf-8 -*-
from odoo import models, fields


class BorrowBooksWarningWizard(models.TransientModel):
    _name = 'borrow.books.warning.wizard'
    _description = 'Borrow Books Warning Wizard'

    borrow_wizard_id = fields.Many2one(comodel_name='borrow.transaction.history', string="Borrow Transaction")
    message = fields.Text(string="Warning Message", readonly=True)
    next_action = fields.Text(string="Next Warning", readonly=True)

    # message = fields.Text(string="Warning Message", readonly=True)

    def action_continue(self):
        """
        Handles the 'Continue' button:
        - If there are more warnings, open the next warning wizard.
        - If no more warnings, continue the borrow transaction.
        """
        if self.next_action:
            # Open the next warning wizard
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warning',
                'res_model': 'borrow.books.warning.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_borrow_wizard_id': self.borrow_wizard_id.id,
                    'default_message': self.next_action[0],  # Show next warning message
                    'default_next_action': self.next_action[1:] if len(self.next_action) > 1 else None
                }
            }
        else:
            # No more warnings, proceed with the borrow transaction
            return self.borrow_wizard_id._process_borrow_transaction()

    def action_cancel(self):
        """
        To delete current record
        """
        record_id = self.env.context.get('active_id')
        self.env["borrow.transaction.history"].browse(record_id).unlink()