# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'
    """
    This model is created for to add one many to many field
    """

    sales_approval_threshold_ids = fields.Many2many('sales.manager.approval',
                                                    'company_approval_threshold_rel',
                                                    'company_id', 'threshold_id',
                                                    string='Sales Approval Thresholds')
