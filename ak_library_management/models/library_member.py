# -*- coding: utf-8 -*-

from odoo import models, fields

class LibraryMember(models.Model):
    """
    The LibraryMember model is used to store detailed information about member in the library
    system.It includes information such as the Member name, Email id, Contact Number,Membership Start Date
    of the book.
    """
    _name = "library.member"
    _description = "Stores library member details"

    # field's name
    name = fields.Char(string='Member name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')

