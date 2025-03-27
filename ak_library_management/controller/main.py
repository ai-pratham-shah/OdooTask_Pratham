# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request,route

class ContactsController(http.Controller):
    """
    Dynamic HTTP controller to create a Contacts webpage
    """
    @http.route('/contacts', type='http', auth="public", website=True)
    def contacts_page(self):
        """
        Render the Kanban-style contacts page.
        """
        contacts = request.env['res.partner'].sudo().search([])
        return request.render("ak_library_management.contacts_page", {'contacts': contacts})

    @http.route('/contacts/<model("res.partner"):partner>', type='http', auth="public", website=True)
    def contact_detail(self, partner):
        """
        Display contact details using slug.
        """
        return request.render("ak_library_management.contact_detail", {'partner': partner})
