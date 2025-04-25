
# models/res_config_settings.py
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_user_onboarding = fields.Boolean(
        string="Enable User Onboarding",
        help="If enabled, new users will go through an onboarding process on first login",
        config_parameter='pratham_frontend_document2.enable_user_onboarding'
    )