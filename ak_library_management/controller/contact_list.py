from odoo import http
from odoo.http import request,route
import unidecode
import re
# from odoo.addons.website.models.website import slug

# class ResPartnerController(http.Controller):
#     @http.route('/contactus', auth='public', website=True)
#     def contact_list(self):
#         partners = request.env['res.partner'].search([])
#         return request.render('ak_library_management.res_partner_template',{
#             'partners': partners
#         })
#
#     @http.route('/contactus/<int:partner_id>', auth='public', website=True)
#     def contact_detail(self, partner_id):
#         partner = request.env['res.partner'].browse(partner_id)
#         if not partner.exists():
#             return request.not_found()
#         return request.render('ak_library_management.res_partner_detail_template', {
#             'partner': partner
#         })

class ContactsController(http.Controller):

    def generate_slug(self, name, record_id):
        """Generate a URL-safe slug from the contact name and ID."""
        slug = unidecode.unidecode(name).lower()
        slug = re.sub(r'\W+', '-', slug)  # Replace non-alphanumeric characters with dashes
        return f"{slug}-{record_id}"

    @http.route('/contacts', type='http', auth="public", website=True)
    def contacts_page(self, **kwargs):
        """Render the Kanban-style contacts page."""
        contacts = request.env['res.partner'].sudo().search([])
        for contact in contacts:
            contact.slug = self.generate_slug(contact.name, contact.id)
        return request.render("ak_library_management.contacts_page", {'contacts': contacts})

    @http.route('/contact/<string:slug>', type='http', auth="public", website=True)
    def contact_detail(self, slug, **kwargs):
        """Display contact details using slug."""
        contact_id = slug.split('-')[-1]  # Extract the last part as ID
        contact = request.env['res.partner'].sudo().browse(int(contact_id))
        if not contact.exists():
            return request.not_found()
        return request.render("ak_library_management.contact_detail", {'contact': contact})
