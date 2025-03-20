from odoo import http
from odoo.http import request,route

class ResPartnerController(http.Controller):
    @http.route('/contactus', auth='public', website=True)
    def contact_list(self):
        partners = request.env['res.partner'].search([])
        return request.render('ak_library_management.res_partner_template',{
            'partners': partners
        })

    @http.route('/contactus/<int:partner_id>', auth='public', website=True)
    def contact_detail(self, partner_id):
        partner = request.env['res.partner'].browse(partner_id)
        if not partner.exists():
            return request.not_found()
        return request.render('ak_library_management.res_partner_detail_template', {
            'partner': partner
        })