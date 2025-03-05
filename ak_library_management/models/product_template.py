# -*- coding: utf-8 -*-


from odoo import models, fields,api
from datetime import date,timedelta
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """
    Inherit product template model from addons and add some custom fields.
    """
    #fields
    is_library_book = fields.Boolean(string='Is library book')
    author = fields.Char(string='Author')
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('unavailable','Unavailable'),
        ('returned','Returned')
    ], 'Status', tracking=True, default='available')
    reference = fields.Char(readonly=True)

    @api.model_create_multi
    def create(self, vals):
        """
        This method is overriding reference filed with sequence number
        """
        res = super().create(vals)
        res.default_code = self.env['ir.sequence'].next_by_code('product.template')
        print('This is default_code:',res.default_code)
        return res

    @api.constrains('unavailable')
    def action_mark_borrowed(self):
        """
        This method is created for marked book as borrowed
        and this method is used in button in xml side
        """
        self.status = 'borrowed'
        for record in self.filtered(lambda r: r.status != 'borrowed'):
            if record.status == 'unavailable':
                raise ValidationError("The book is marked as 'Unavailable' and cannot be borrowed.")
            record.message_post(
                body=f"The book was borrowed by {self.env.user.name} on {fields.Datetime.now()}",
                subject="Book Borrowed",
            )
        date_deadline = date.today() + timedelta(days=10)
        return super().activity_schedule(date_deadline=date_deadline,
                                         summary=f'book borrowed by {self.env.user.name} '
                                                 f'and return date {date_deadline}')

    def action_mark_available(self):
        """
        This method is created for marked book as available
        and this method is used in button in xml side
        """
        self.status = 'available'

    def _compute_display_name(self):
        """
        override compute display name and change book name format to
        [author_name]book_name.
        """
        for record in self:
            # Use f-string for better readability and performance
            if self._context.get('add_author') and record.author:
                record.display_name = f"[{record.author}] {record.name}"
            else:
                record.display_name = record.name
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=None):
        """Override name_search method to search book by author name."""
        # Ensure 'args' is a list if it is None
        args = args or []
        if name:
            # Add condition to search by author
            args.append(('author', operator, name))

        # Call the parent method with updated arguments
        return super().name_search(name='', args=args, operator=operator, limit=limit)
    def action_borrow_books(self):
        """Open the borrow books wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_borrow_book_returned(self):
        """
        Using this method can change the state into returned.
        """
        self.write({'status': 'returned'})
        self.message_post(
            body=f'{self.env.user.name} returned the book. Date: {date.today()}',
            subject="Book Returned",
            message_type="comment"
        )

    @api.constrains('status')
    def _check_return_book(self):
        """
        Using this function we can generate simple
        notification when state of book is change.
        """
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': 'warning',
            'message': f"{self.name} product state is changed to {self.status}",
        })

    def mark_as_returned(self):
        """
        Marks the book or transaction as 'returned' by updating the status field.

        This method changes the status of the current record to 'returned',
        indicating that the borrowed book has been returned to the library.

        Returns:
            bool: True if the status is successfully updated, otherwise False.
        """
        self.write({'status': 'returned'})