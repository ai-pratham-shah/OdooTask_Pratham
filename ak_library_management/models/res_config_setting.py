# -*- coding: utf-8 -*-

from odoo import models, fields


class LibraryConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    borrowing_limit = fields.Integer(
        string="Max Borrowing Limit",
        config_parameter='ak_library_management.borrowing_limit',
        default=5
    )
