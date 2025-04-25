
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Additional fields for partners associated with users
    date_of_birth = fields.Date(string="Date of Birth", related='user_ids.date_of_birth', store=True)
    place_of_birth = fields.Char(string="Place of Birth", related='user_ids.place_of_birth', store=True)
    gender = fields.Selection(related='user_ids.gender', store=True)
    passport_number = fields.Char(string="Passport Number", related='user_ids.passport_number', store=True)
    driving_license = fields.Char(string="Driving License", related='user_ids.driving_license', store=True)
    speaking_language = fields.Selection(related='user_ids.speaking_language', store=True)
    marital_status = fields.Selection(related='user_ids.marital_status', store=True)
