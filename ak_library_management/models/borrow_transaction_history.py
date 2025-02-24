# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BorrowTransactionHistory(models.Model):
    _name = 'borrow.transaction.history'
    _description = 'Borrow Transaction History'
    _rec_name = 'customer_id'

    #fields
    customer_id = fields.Many2one('res.partner',
                                  "Customer", required=True)
    books_ids = fields.Many2many('product.template',
                             string="Books", required=True, domain="[('is_library_book' ,'=', True)]")
    borrow_start_date = fields.Datetime(string="Borrow Start Date",
                                        default=fields.Datetime.now, required=True)
    borrow_end_date = fields.Datetime("Borrow End Date",
                                      required=True)
    deposit_amount = fields.Float("Deposit Amount")
    is_member = fields.Boolean(related="customer_id.is_member")

    @api.constrains('borrow_end_date','borrow_start_date')
    def _check_borrow_end_date(self):
        """
        Ensures that the borrow_end_date is greater than or equal to the borrow_start_date.
        """
        for record in self:
            if record.borrow_end_date < record.borrow_start_date:
                raise ValidationError("Borrow End Date must be greater than or equal to Borrow Start Date.")

    def action_confirm(self):
        """
        Confirms the book borrowing process after performing the necessary checks.
        - If any warning conditions are met, a warning wizard is shown.
        - If no warnings exist, it creates a borrow transaction and updates stock.
        """
        # Check 1: Customer Trustworthiness
        if self.customer_id.not_trust_worthy:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warning',
                'res_model': 'borrow.books.warning.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_borrow_wizard_id': self.id,
                    'default_message': '\n'"Customer is not trustworthy. Are you sure you want to continue?",
                }
            }
        # Check 2: Product Availability
        out_of_stock_books = self.books_ids.filtered(lambda book: book.qty_available <= 0)
        if out_of_stock_books:
            out_of_stock_names = ', '.join(out_of_stock_books.mapped('name'))
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warning',
                'res_model': 'borrow.books.warning.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    # 'default_borrow_wizard_id': self.id,
                    'default_message': '\n'f"The following books are out of stock: {out_of_stock_names}. Are you sure you want to continue?",
                }
            }
        # Check 3: Maximum Books Borrowed
        if len(self.books_ids) > 5:
            # Case A: Check for existing open borrow transactions
            open_borrow_transactions = self.env['borrow.transaction.history'].search([
                ('customer_id', '=', self.customer_id.id),
                ('borrow_end_date', '>', fields.Datetime.now())  # Only check for open transactions
            ])

            if open_borrow_transactions:
                # Calculate total books in open borrow transactions
                open_books_count = sum(len(transaction.books_ids) for transaction in open_borrow_transactions)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Warning',
                    'res_model': 'borrow.books.warning.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_message': '\n' f"Customer already has {len(open_borrow_transactions)} open borrow transactions with "
                                            f"{open_books_count} books. Are you sure you want to borrow more books?",
                        }
                    }
            else:
                # Case B: No open borrow transactions exist
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Warning',
                    'res_model': 'borrow.books.warning.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_message': '\n' "Are you sure you want to allow borrowing more than 5 books for this customer?",
                    }
                }
        for book in self.books_ids:
            if book.qty_available > 0:  # Ensure stock is available
                book.qty_available -= 1

        return {'type': 'ir.actions.act_window_close'}
