# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import RedirectWarning


class BorrowBooksWizard(models.TransientModel):
    _name = 'borrow.books.wizard'
    _description = 'Borrow Books Wizard'

    customer_id = fields.Many2one('res.partner', string='Customer Name', required=True)
    from_datetime = fields.Datetime(string='From Datetime', default=fields.Datetime.now, required=True)
    end_datetime = fields.Datetime(string='End Datetime', required=True)
    book_ids = fields.Many2many('product.template', string='Books', domain=[('is_library_book', '=', True)])
    deposit_amount = fields.Float(string='Deposit Amount')
    is_member = fields.Boolean(related="customer_id.is_member")

    # Button action to confirm the borrowing process
    def action_confirm(self):
        # Check 1: Customer Trustworthiness
        if self.customer_id.not_trust_worthy:
            # Show a RedirectWarning if the customer is marked as not trustworthy
            raise RedirectWarning(
                _('Customer is not trustworthy. Are you sure you want to continue?'),
                self._borrow_books,
                'Continue',
                # 'Cancel'
            )
            return {
                'type': 'ir.actions.act_window',
                'name': 'Borrow Books Wizard',
                'res_model': 'borrow.books.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('ak_library_management.borrow.books.wizard.form').id,
                'target': 'new',
            }

        # Check 2: Product Availability
        out_of_stock_books = [book for book in self.book_ids if book.available == 0]
        if out_of_stock_books:
            out_of_stock_names = ", ".join([book.name for book in out_of_stock_books])
            raise RedirectWarning(
                f"The following books are out of stock: {out_of_stock_names}. Are you sure you want to continue?",
                self._borrow_books,
                'Continue',
                _('Cancel')
            )

        # Check 3: Maximum Books Borrowed
        if len(self.book_ids) > 5:
            open_transactions = self.env['borrow.transaction.history'].search(
                [('customer_id', '=', self.customer_id.id), ('status', '=', 'open')]
            )
            if open_transactions:
                raise RedirectWarning(
                    f"Customer already has {len(open_transactions)} open borrow transactions with {len(self.book_ids)} books. Are you sure you want to borrow more books?",
                    self._borrow_books,
                    'Continue',
                    _('Cancel')
                )
            else:
                raise RedirectWarning(
                    "Are you sure you want to allow borrowing more than 5 books for this customer?",
                    self._borrow_books,
                    _('Continue'),
                    _('Cancel')
                )

        # If no issues, proceed
        self._borrow_books()

        # The action method that will be called when the user clicks 'Continue'

    def _borrow_books_action(self):
        return self._borrow_books()

    # Method to handle the borrowing process after confirmation
    def _borrow_books(self):
        # Create the borrow transaction record
        self.env['borrow.transaction.history'].create({
            'customer_id': self.customer_id.id,
            'from_datetime': self.from_datetime,
            'end_datetime': self.end_datetime,
            'book_ids': [(6, 0, self.book_ids.ids)],
            'deposit_amount': self.deposit_amount,
        })

        # Decrease the stock for each borrowed book
        for book in self.book_ids:
            if book.available > 0:
                book.available -= 1
                book.status = 'borrowed'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books Wizard',
            'res_model': 'borrow.books.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('borrow_book_wizard.borrow.books.wizard.form'),
            'target': 'new',
        }

    # Helper method to show the confirmation warning
    # def _confirm_warning(self, message, action):
    #     return self.env['res.partner'].browse([self.customer_id.id]).message_post(
    #         body=message,
    #         subtype_xmlid='mail.mt_comment'
    #     )