# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BorrowTransactionHistory(models.Model):
    _name = 'borrow.transaction.history'
    _description = 'Borrow Transaction History'

    #fields
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    books = fields.Many2many('product.template', string="Books", required=True)
    borrow_start_date = fields.Datetime(string="Borrow Start Date", default=fields.Datetime.now, required=True)
    borrow_end_date = fields.Datetime(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount", compute="_compute_deposit_amount", store=True)

