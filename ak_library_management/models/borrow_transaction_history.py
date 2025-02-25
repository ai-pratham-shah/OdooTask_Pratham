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
    deposit_amount = fields.Float("Deposit Amount", required=True)
    is_member = fields.Boolean(related="customer_id.is_member")

    @api.constrains('borrow_end_date','borrow_start_date')
    def _check_borrow_end_date(self):
        """
        Ensures that the borrow_end_date is greater than or equal to the borrow_start_date.
        """
        if self.borrow_end_date < self.borrow_start_date:
             raise ValidationError("Borrow End Date must be greater than or equal to Borrow Start Date.")

    def action_confirm(self):
        """
        Confirms the book borrowing process after performing the necessary checks.
        - If any warning conditions are met, a warning wizard is shown.
        - If no warnings exist, it creates a borrow transaction and updates stock.
        """
        def show_warning_wizard(message):
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warning',
                'res_model': 'borrow.books.warning.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_borrow_wizard_id': self.id,
                    'default_message': message,
                }
            }

        # Check 1: Customer Trustworthiness
        if self.customer_id.not_trust_worthy:
            return show_warning_wizard(
                "Customer is not trustworthy. Are you sure you want to continue?"
            )

        # Check 2: Product Availability
        out_of_stock_books = self.books_ids.filtered(lambda book: book.qty_available <= 0)
        if out_of_stock_books:
            out_of_stock_names = ', '.join(out_of_stock_books.mapped('name'))
            return show_warning_wizard(
                f"The following books are out of stock: {out_of_stock_names}. Are you sure you want to continue?"
            )

        # Check 3: Maximum Books Borrowed
        if len(self.books_ids) > 5:
            # Case A: Check for existing open borrow transactions
            open_borrow_transactions = self.env['borrow.transaction.history'].search([
                ('customer_id', '=', self.customer_id.id),
                ('borrow_end_date', '>', fields.Datetime.now())  # Only check for open transactions
            ])

            if open_borrow_transactions:
                open_books_count = sum(len(transaction.books_ids) for transaction in open_borrow_transactions)
                return show_warning_wizard(
                    f"Customer already has {len(open_borrow_transactions)} open borrow transactions with "
                    f"{open_books_count} books. Are you sure you want to borrow more books?"
                )
        else:
            # Case B: No open borrow transactions exist
            return show_warning_wizard(
                "Are you sure you want to allow borrowing more than 5 books for this customer?"
            )
        for record in self.books_ids:
            if record.qty_available:
                record.qty_available -= 1