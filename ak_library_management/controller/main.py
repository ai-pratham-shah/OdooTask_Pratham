# -*- coding: utf-8 -*-
from PyKCS11.LowLevel import FALSE
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

class CustomerController(http.Controller):

    @http.route('/customer_page', type='http', auth="public", website=True, csrf=False)
    def customer_page(self, **args):
        return request.render("ak_library_management.customer_fetch_page")

    @http.route('/customer_page/get_customer', type='json', auth='public', csrf=False)
    def get_customer(self, **args):
        email = args.get('email')
        if not email:
            return {'error': 'Email is required'}

        customer = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        if customer:
            return {
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone or 'N/A',
            }
        return {'error': 'Customer not found'}
