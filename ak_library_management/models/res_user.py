# -*- coding: utf-8 -*-

from odoo import models,fields


class Users(models.Model):
    """
    Inherit res users to add boolean field
    for perform some operations.
    """
    _inherit = 'res.users'

    is_manager = fields.Boolean(string="Is Manager")
