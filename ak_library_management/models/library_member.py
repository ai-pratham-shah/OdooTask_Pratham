# -*- coding: utf-8 -*-

from odoo import models, fields

class LibraryMember(models.Model):
    _name = "library.member"
    _description = "Stores library member details"
    _rec_name = "name"

    # field's name
    name = fields.Char(string='Member name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')

