# -*- coding: utf-8 -*-

from odoo import models, fields


class LibraryMember(models.Model):
    _name = "library.member"
    _description = "Stores library member details"

    name = fields.Char(string='Member name')
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')

