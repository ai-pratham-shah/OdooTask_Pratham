# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import AccessError


class LibraryMember(models.Model):
    """
    The LibraryMember model is used to store detailed information
    about member in the library system.It includes information
    such as the Member name, Email id, Contact Number,Membership Start Date
    of the book.
    """
    _name = "library.member"
    _description = "Stores library member details"
    _inherit = ['mail.thread']

    # field's name
    name = fields.Char('Member name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    membership_no = fields.Char(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        """
        inherit the create method and update sequence number.
        """
        for val in vals_list:
            val['membership_no'] = self.env["ir.sequence"].next_by_code('library.member')
        return super().create(vals_list)

    def action_send_renewal_email(self):
        """
        Opens the email compose wizard for the selected library member.
        Preloads the email with a renewal reminder template that can be
        edited by the librarian before sending.
        """
        self.ensure_one()
        librarian_user = self.env.user
        if not librarian_user.is_librarian:
            raise AccessError("You are not authorized to send an email from this library member.")
        template_id = self.env.ref('ak_library_management.library_membership_renewal_reminder_email_template').id
        composer = {
            'default_template_id': template_id,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': composer,
        }
