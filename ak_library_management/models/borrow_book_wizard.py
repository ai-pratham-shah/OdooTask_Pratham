# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BorrowBooksWizard(models.TransientModel):
    """
    Wizard for borrowing books with the following validations:
    1. Customer Trustworthiness Check.
    2. Product Availability Check.
    3. Maximum Books Borrowed Check.
    """

    _name = 'borrow.books.wizard'
    _inherit = 'borrow.transaction.history'  # Inheriting borrow.transaction.history model
    _description = 'Borrow Books Wizard'

    # You can inherit the fields from borrow.transaction.history
    # borrow_start_date, borrow_end_date, customer_id, deposit_amount, books are already inherited.

    # book_ids = fields.Many2many('product.template', string='Books', required=True)
    # deposit_amount = fields.Float(string='Deposit Amount')

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
        out_of_stock_books = self.book_ids.filtered(lambda book: book.qty_available <= 0)
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
        if len(self.book_ids) > 5:
            open_borrow_transactions = self.env['borrow.transaction.history'].search([
                ('customer_id', '=', self.customer_id.id),
                ('borrow_end_date', '>', fields.Datetime.now())
            ])

            if open_borrow_transactions:
                open_books_count = sum(len(transaction.books) for transaction in open_borrow_transactions)
                # warning_messages.append(
                #     f"Customer already has {len(open_borrow_transactions)} open borrow transactions with "
                #     f"{open_books_count} books. Are you sure you want to borrow more books?")
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Warning',
                    'res_model': 'borrow.books.warning.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        # 'default_borrow_wizard_id': self.id,
                        'default_message': '\n'"Are you sure you want to allow borrowing more than 5 books for this customer?",
                    }
                }

        # If all checks pass, proceed with saving the transaction
        self._create_borrow_transaction()
        return {'type': 'ir.actions.act_window_close'}

    def _create_borrow_transaction(self):
        """
        Creates a new record in `borrow_transaction_history` and updates stock.
        - Reduces the stock quantity by 1 for each borrowed book.
        - Applies a deposit amount if the customer is not a member.
        """

        borrow_record = self.env['borrow.transaction.history'].create({
            'customer_id': self.customer_id.id,
            'books': [(6, 0, self.book_ids.ids)],
            'borrow_start_date': self.borrow_start_date,
            'borrow_end_date': self.borrow_end_date,
            'deposit_amount': self.deposit_amount
        })

        # Reduce stock quantity by 1 for each borrowed book
        for book in self.book_ids:
            book.qty_available -= 1
