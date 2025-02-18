# -*- coding: utf-8 -*-
from odoo import models, fields
class SaleOrderApprovalWizard(models.TransientModel):
    """
    To show dynamic message to the user in wizard.
    """
    _name = 'sale.order.approval.wizard'
    _description = 'Sale Order Approval Wizard'

    message = fields.Text(readonly=True)  # Field to hold the dynamic message
