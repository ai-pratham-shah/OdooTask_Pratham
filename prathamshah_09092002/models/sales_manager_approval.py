# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SalesManagerApproval(models.Model):
    _name = 'sales.manager.approval'
    _description = 'Sales Manager Approval Configuration'
    _rec_name = 'sales_manager_id'
    """
    This model is created for perform some approval related operations.
    """

    sales_manager_id = fields.Many2one('res.users', string='Sales Manager', required=True)
    approval_threshold = fields.Monetary(string='Approval Threshold Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('sales_manager_uniq', 'unique(sales_manager_id, approval_threshold)',
         'A threshold with this configuration already exists!')
    ]

    @api.constrains('approval_threshold')
    def _check_threshold_amount(self):
        for record in self:
            existing = self.search([
                ('approval_threshold', '=', record.approval_threshold),
                ('currency_id', '=', record.currency_id.id),
                ('company_id', '=', record.company_id.id),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(_("Threshold amount %s is already configured!"))
