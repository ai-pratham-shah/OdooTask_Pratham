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
    books = fields.Many2many('product.template',
                             string="Books", required=True)
    borrow_start_date = fields.Datetime(string="Borrow Start Date",
                                        default=fields.Datetime.now, required=True)
    borrow_end_date = fields.Datetime("Borrow End Date",
                                      required=True)
    deposit_amount = fields.Float("Deposit Amount")
    is_member = fields.Boolean(related="customer_id.is_member")
    # deposit_amount = fields.Float("Deposit Amount", compute="_compute_deposit_amount", store=True)
    # @api.depends('customer_id.is_member')
    # def _compute_deposit_amount(self):
    #     """
    #     Conditional deposit amount based on whether the customer is a member or not.
    #     If the customer is a member, no deposit is required.
    #     """
    #     for record in self:
    #         # Only visible and required if customer is not a member
    #         if not record.customer_id.is_member:
    #             record.deposit_amount = 100.0  # Set a default deposit amount if not a member
    #         else:
    #             record.deposit_amount = 0.0  # No deposit required for members

    @api.constrains('borrow_end_date','borrow_start_date')
    def _check_borrow_end_date(self):
        """
        Ensures that the borrow_end_date is greater than or equal to the borrow_start_date.
        """
        for record in self:
            if record.borrow_end_date < record.borrow_start_date:
                raise ValidationError("Borrow End Date must be greater than or equal to Borrow Start Date.")

