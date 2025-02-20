# -*- coding: utf-8 -*-

from odoo import models, fields,api

class LibraryMember(models.Model):
    """
    The LibraryMember model is used to store detailed information
    about member in the library system.It includes information
    such as the Member name, Email id, Contact Number,Membership Start Date
    of the book.
    """
    _name = "library.member"
    _description = "Stores library member details"

    # field's name
    name = fields.Char('Member name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    membership_no = fields.Char(readonly=True)

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        res.membership_no = self.env['ir.sequence'].next_by_code('library.member')
        print('This is default_code:', res.membership_no)
        return res