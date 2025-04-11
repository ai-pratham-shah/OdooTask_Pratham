# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    """
    Inherits mrp.production and adds custom field.
    """
    _inherit = 'mrp.production'

    job_name = fields.Char(string='Job Name')
    job_name_readonly = fields.Boolean(compute='_compute_job_name_readonly')

    @api.depends('origin', 'job_name')
    def _compute_job_name_readonly(self):
        for record in self:
            # job_name is readonly if this MO is linked to a sale order
            record.job_name_readonly = bool(record.origin and record.job_name)
