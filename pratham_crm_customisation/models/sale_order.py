# -*- coding: utf-8 -*-


from odoo import models, fields, api

class SaleOrder(models.Model):
    """
    Inherits sale.order and adds custom field.
    """
    _inherit = 'sale.order'

    opportunity_id = fields.Many2one('crm.lead')
    job_name = fields.Char(string="Job Name", compute='_compute_job_name', store=True, readonly=False)
    job_name_readonly = fields.Boolean(compute='_compute_job_name_readonly')

    @api.depends('opportunity_id', 'job_name')
    def _compute_job_name_readonly(self):
        for record in self:
            # job_name is readonly if this sale order is linked to a CRM lead
            record.job_name_readonly = bool(record.opportunity_id and record.job_name)

    @api.depends('opportunity_id')
    def _compute_job_name(self):
        for order in self:
            order.job_name = order.opportunity_id.name if order.opportunity_id else ''

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            job = order.job_name
            order_name = order.name

            # update job name of stock.picking
            deliveries = self.env['stock.picking'].search([('origin', '=', order_name)])
            deliveries.write({'job_name': job})

            # update job name of mrp.production
            mfg_orders = self.env['mrp.production'].search([('origin', '=', order_name)])
            mfg_orders.write({'job_name': job})

            # update job name of project.project
            projects = self.env['project.project'].search([('sale_order_id', '=', order.id)])
            for project in projects:
                project.write({
                    'name': f"{order_name} - {job}",
                    'job_name': job,
                })

        return res
