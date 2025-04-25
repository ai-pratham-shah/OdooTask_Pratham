from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Additional fields for onboarding
    date_of_birth = fields.Date(string="Date of Birth")
    place_of_birth = fields.Char(string="Place of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    mobile_number = fields.Char(string="Mobile Number")
    passport_number = fields.Char(string="Passport Number")
    driving_license = fields.Char(string="Driving License")
    speaking_language = fields.Selection([
        ('gujarati', 'Gujarati'),
        ('hindi', 'Hindi'),
        ('english', 'English')
    ], string="Speaking Language")
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married')
    ], string="Marital Status")
    job_position = fields.Char(string="Job Position")
    onboarding_completed = fields.Boolean(string="Onboarding Completed", default=False)

    def _update_partner_from_onboarding_details(self, vals):
        """Update the partner record with details from onboarding"""
        partner_vals = {}

        # Map user fields to partner fields
        if 'mobile_number' in vals:
            partner_vals['mobile'] = vals['mobile_number']

        # Add other fields that are relevant to the partner
        if partner_vals:
            self.partner_id.sudo().write(partner_vals)

    @api.model_create_multi
    def create(self, vals_list):
        users = super(ResUsers, self).create(vals_list)

        for user, vals in zip(users, vals_list):
            if vals.get('onboarding_details'):
                user._update_partner_from_onboarding_details(vals['onboarding_details'])

        return users

    def write(self, vals):
        res = super(ResUsers, self).write(vals)

        if 'onboarding_details' in vals:
            self._update_partner_from_onboarding_details(vals['onboarding_details'])

        return res