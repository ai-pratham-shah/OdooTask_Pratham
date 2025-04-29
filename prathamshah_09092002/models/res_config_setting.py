# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    """
    This model is created to add one many to many fields.
    """

    sales_approval_threshold_ids = fields.Many2many('sales.manager.approval',
                                                    string='Sales Approval Thresholds',
                                                    related='company_id.'
                                                            'sales_approval_threshold_ids',
                                                    readonly=False)
