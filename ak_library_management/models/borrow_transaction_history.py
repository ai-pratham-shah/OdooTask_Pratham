# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta, date, datetime


class BorrowTransactionHistory(models.Model):
    _name = 'borrow.transaction.history'
    _description = 'Borrow Transaction History'
    _inherit = ['mail.thread']
    _rec_name = 'customer_id'

    # fields
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string="Customer", required=True)
    books_ids = fields.Many2many(comodel_name='product.template',
                                 string="Books", required=True,
                                 domain="[('is_library_book' ,'=', True)]")
    borrow_start_date = fields.Date(string="Borrow Start Date",
                                      default=fields.Datetime.now, required=True)
    borrow_end_date = fields.Date(string="Borrow End Date",
                                  required=True)
    deposit_amount = fields.Float(string="Deposit Amount", required=True)
    is_member = fields.Boolean(related="customer_id.is_member")
    is_returned = fields.Boolean(string="Returned", default=False)
    is_active = fields.Boolean(compute='_compute_active_transaction', store=True)

    @api.depends('borrow_end_date')
    def _compute_active_transaction(self):
        """
        check the transaction is active or not and set true or false in boolean field
        param: None
        rtype: None
        """
        for rec in self.search([]):
            rec.is_active = rec.borrow_end_date >= date.today()

    @api.constrains('borrow_end_date', 'borrow_start_date')
    def _check_borrow_end_date(self):
        """
        Ensures that the borrow_end_date is greater
        than or equal to the borrow_start_date.
        """
        if self.borrow_end_date < self.borrow_start_date:
            raise ValidationError("Borrow End Date must be greater "
                                  "than or equal to Borrow Start Date.")

    def show_warning_wizard(self, message, next_action=None):
        """
        Helper function to return a warning wizard action.
        This function is now defined as a separate method to improve code structure.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warning',
            'res_model': 'borrow.books.warning.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_wizard_id': self.id,
                'default_message': message,  # Show the current warning message
                'default_next_action':  repr(next_action) if next_action else None,  # Pass the next warnings (remaining warnings)
            }
        }

    def action_confirm(self):
        """ Confirms the book borrowing process after performing the necessary checks. """
        warnings = []

        # **Check 1: Customer Trustworthiness**
        if self.customer_id.not_trust_worthy:
            warnings.append("Customer is not trustworthy. Are you sure you want to continue?")

        # **Check 2: Product Availability (books out of stock)**
        out_of_stock_books = self.books_ids.filtered(lambda book: book.qty_available <= 0)
        if out_of_stock_books:
            book_names = ", ".join(out_of_stock_books.mapped('name'))  # Get book names
            warnings.append(f"The following books are out of stock: {book_names}.")

        # **Check 3: Borrowing More Than 5 Books**
        if len(self.books_ids) >= 5:
            search_recd = self.search([('customer_id.id', "=", self.customer_id.id)], order='id desc', offset=1)
            books_name = {book.name for rec in search_recd for book in rec.books_ids}
            if books_name:
                warnings.append(f"Customer already has [{len(search_recd)}] open borrow transactions with "
                                f"{', '.join(books_name)} books. Are you sure you want to borrow more books?")
            else:
                warnings.append("Are you sure you want to allow borrowing more than 5 books for this customer?")

        # **Display warnings sequentially**
        if warnings:
            return self.show_warning_wizard(warnings[0], next_action=warnings[1:] if len(warnings) > 1 else None)
        else:
            # No warnings, proceed with the borrow transaction
            return self._process_borrow_transaction()

    def _process_borrow_transaction(self):
        """Finalizes the borrow transaction and updates stock quantities."""
        for rec in self.books_ids:
            loca = self.env['stock.quant'].search([('product_tmpl_id.id', '=', rec.id)], limit=1)
            if loca:
                new_qty = -1 if rec.qty_available <= 0 else -1
                self.env['stock.quant']._update_available_quantity(loca.product_id, loca.location_id, quantity=new_qty)
        return True

    def send_book_return_reminders(self):
        """
        Scheduled action: that runs daily and sends reminders for books
        that are due in exactly 2 days.
        """
        reminder_date = date.today() + timedelta(days=2)
        records = self.search([
            ('borrow_end_date', '=', reminder_date),
            ('is_returned', '=', False)
        ])

        template = self.env.ref('ak_library_management.book_return_reminder_email_template')
        if not template:
            raise UserError("Email template for book return reminder is not defined!")

        for record in records:
            if any(book.status == 'borrowed' for book in record.books_ids):
                template.send_mail(record.id, force_send=True)

    def mark_books_as_returned(self):
        """
        server action:
        Marks books as returned and notifies the customer.
        Args:
            None
        Returns:
            None
        """
        for rec in self:
            # Mark transaction as returned
            rec.is_returned = True
            # Send notification to the customer
            self.env['bus.bus']._sendone(
                rec.customer_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"Dear {rec.customer_id.name}, your returned book(s) have been recorded.",
                }
            )
            # Mark each book as returned (assuming books have a method to mark them as returned)
            for book in rec.books_ids:
                book.mark_as_returned()
            # Log the action in chatter
            rec.message_post(body=f"Books returned by {rec.customer_id.name}. Transaction marked as completed.")

    def check_overdue_books_action(self):
        """
        Automated action:
        Check if the customer has any overdue borrowed books
        and raise a validation error if there are any overdue items.
        The customer will not be able to borrow new books
        until all overdue items are returned.
        """
        # Fetch all previous borrow transactions for the customer excluding the latest one
        overdue_books = self.search([('customer_id.id', '=', self.customer_id.id)],
                                    order='id desc', offset=1).filtered(
            lambda rec: rec.borrow_end_date < date.today() and
                        any(book.status == "borrowed" for book in rec.books_ids)
        )
        # If any overdue book exists, raise a validation error
        if overdue_books:
            raise ValidationError(f"{overdue_books[0].customer_id.name} has overdue books and cannot borrow new ones "
                                  f"until all overdue items are returned.")

    def send_overdue_book_reminder(self):
        """
        Function to check for overdue books and send reminder emails to customers
        """
        today = datetime.today().date()
        overdue_books = self.search([
            ('borrow_end_date', '<', today),  # Check if the borrow end date is in the past
            ('books_ids.status', '=', 'borrowed')  # Check if the book has not been returned
        ])
        for record in overdue_books:
            # Prepare the email content
            email_template = self.env.ref('ak_library_management.book_return_reminder_email_template')
            if email_template:
                # Send the email
                email_template.send_mail(record.id, force_send=True)
            
