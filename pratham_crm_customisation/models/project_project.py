# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    """
    Inherits project.project and adds custom field.
    """
    _inherit = 'project.project'

    sale_order_id = fields.Many2one('sale.order')
    job_name = fields.Char(string='Job Name')
    job_name_readonly = fields.Boolean(compute='_compute_job_name_readonly')

    @api.depends('sale_order_id', 'job_name')
    def _compute_job_name_readonly(self):
        for record in self:
            # job_name is readonly if this project is linked to a sale order
            record.job_name_readonly = bool(record.sale_order_id and record.job_name)
