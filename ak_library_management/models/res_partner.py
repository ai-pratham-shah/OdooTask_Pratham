# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    not_trust_worthy = fields.Boolean("Not Trustworthy", help="Indicates if the customer is trustworthy or not.")
    is_member = fields.Boolean("Is Member", help="Indicates whether the customer is a member.")
