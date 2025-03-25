# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    """
    Inherit res partner model to add some custom fields.
    """

    not_trust_worthy = fields.Boolean(string="Not Trustworthy", help="Indicates if the customer is trustworthy or not.")
    is_member = fields.Boolean(string="Is Member", help="Indicates whether the customer is a member.")
    slug = fields.Char(string='Slug', store=True)
