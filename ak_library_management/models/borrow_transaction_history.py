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

    @api.constrains('borrow_end_date', 'borrow_start_date')
    def _check_borrow_end_date(self):
        """
        Ensures that the borrow_end_date is greater
        than or equal to the borrow_start_date.
        """
        if self.borrow_end_date < self.borrow_start_date:
            raise ValidationError("Borrow End Date must be greater "
                                  "than or equal to Borrow Start Date.")

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

        # To decreased on hand qty.
        for rec in self.books_ids.filtered(lambda book: book.qty_available):
            loca = self.env['stock.quant'].search([('product_tmpl_id.id', '=', rec.id)], limit=1)
            if loca:
                self.env['stock.quant']._update_available_quantity(loca.product_id, loca.location_id, quantity=-1)

        # Check 1: Customer Trustworthiness
        if self.customer_id.not_trust_worthy:
            return show_warning_wizard(
                "Customer is not trustworthy. "
                "Are you sure you want to continue?"
            )

        # Check 2: Product Availability
        out_of_stock_books = (
            self.books_ids.filtered(lambda book: book.qty_available <= 0))
        if out_of_stock_books:
            return show_warning_wizard(
                f"The following books are out of stock:{', '.join(out_of_stock_books.mapped('name'))}."
                f"Are you sure you want to continue?"
            )

        # Check 3: when customer is trying to borrow 5 or more books
        if len(self.books_ids) >= 5:
            search_recd = self.search([('customer_id.id', "=", self.customer_id.id)], order='id desc', offset=1)
            books_name = {book.name for rec in search_recd for book in rec.books_ids}
            if books_name:
                return show_warning_wizard(
                                        f"Customer already has [{len(search_recd)}] "
                                        f"open borrow transactions "
                                        f"with {books_name} books. "
                                        f"Are you sure you want to borrow more books?")
            return show_warning_wizard(
                                    "Are you sure you want to allow "
                                    "borrowing more than 5 books for this customer?")

    def send_book_return_reminders(self):
        """
        Scheduled action that runs daily and sends reminders for books
        that are due in exactly 2 days.
        Args:
            None
        Returns:
            None
        """
        all_recd = self.search([])
        for record in all_recd:
            for rec in record.books_ids:
                if rec.status == 'borrowed':
                    date_deadline = record.borrow_start_date + timedelta(days=2)
                    if record.borrow_end_date == date_deadline:
                        self.env['bus.bus']._sendone(record.customer_id, 'simple_notification', {
                            'type': 'warning',
                            'message': f"reminder: your book return date is {record.borrow_end_date}",
                        })
                        record.message_post(
                            body=f"Reminder sent to {record.customer_id.name} "
                                 f"for book return on {record.borrow_end_date}.")

    def mark_books_as_returned(self):
        """
        Marks books as returned and notifies the customer
        Args:
            None
        Returns:
            None
        """
        for rec in self:
            if rec.is_returned:
                raise UserError(f"Books for {rec.customer_id.name} "
                                f"have already been marked as returned.")
            rec.is_returned = True  # Mark transaction as returned
            # Send notification to the customer
            self.env['bus.bus']._sendone(
                rec.customer_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"Dear {rec.customer_id.name},"
                               f"your returned book(s) have been recorded.",
                })
            # Mark each book as returned
            for book in rec.books_ids:
                book.mark_as_returned()
            # Log the action in chatter
            rec.message_post(body=f"Books returned by {rec.customer_id.name}."
                                  f"Transaction marked as completed.")


    def check_overdue_books_action(self):
        """
        Check if the customer has any overdue borrowed books
        and raise a validation error if there are any overdue items.
        The customer will not be able to borrow new books
        until all overdue items are returned.

        Args:
            None
        Returns:
            None
        Raises:
            ValidationError: If there are overdue books for the customer.
        """
        # Search for all borrow transactions for the customer excluding the latest one
        search_rec = self.search([('customer_id', '=', self.customer_id.id)])

        # Loop through all records except the last one (latest borrow transaction)
        for rec in search_rec[:-1]:
            # Loop through all borrowed books in the transaction
            for book in rec.books_ids:
                # Check if the book is overdue and still borrowed
                if rec.borrow_end_date < date.today() and book.status == "borrowed":
                    raise ValidationError(
                        f"{rec.customer_id.name} has overdue books and cannot borrow new ones "
                        f"until all overdue items are returned."
                    )

    def send_overdue_book_reminder(self):
        """Function to check for overdue books and send reminder emails to customers"""
        today = datetime.today().date()
        overdue_books = self.search([
            ('borrow_end_date', '<', today),  # Check if the borrow end date is in the past
            ('is_returned', '=', False)  # Check if the book has not been returned
        ])

        for record in overdue_books:
            # Prepare the email content
            email_template = self.env.ref('ak_library_management.book_return_reminder_email_template')
            if email_template:
                # Send the email
                email_template.send_mail(record.id, force_send=True)
            else:
                raise UserError("Email template for overdue book reminder is not defined!")
