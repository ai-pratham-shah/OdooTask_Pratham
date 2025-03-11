# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryWarehouse(models.Model):
    _inherit = 'stock.warehouse'  # Inheriting base warehouse model

    library_assistant = fields.Many2one(
        'hr.employee',
        string="Library Assistant",
        help="Assign a single Library Assistant."
    )

    workers_ids = fields.Many2many(
        'hr.employee',
        string="Library Workers",
        help="Assign multiple Library Workers."
    )

    @api.constrains('library_assistant', 'workers_ids')
    def _check_unique_assignments(self):
        """
        Ensures that an employee cannot be both a Library Assistant and a Worker in the same warehouse.
        """
        for record in self:
            if record.library_assistant and record.library_assistant in record.workers_ids:
                raise ValidationError("A Library Assistant cannot also be a Worker in the same warehouse.")
