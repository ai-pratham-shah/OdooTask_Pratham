# -*- coding: utf-8 -*-

from odoo import models,fields
class Users(models.Model):
    _inherit = 'res.users'

    is_manager = fields.Boolean(string="Is Manager")
