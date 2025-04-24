# -*- coding: utf-8 -*-

import zipfile
import io
import base64
import re
from odoo import http
from odoo.http import request, route


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

    @http.route('/contacts/<path:slug_url>', type='http', auth="public", website=True)
    def contact_detail(self, slug_url, **kwargs):
        """
        Display contact details using slug.
        """
        partner_id = int(slug_url.split('-')[-1])
        partner = request.env['res.partner'].sudo().browse(partner_id)

        if not partner.exists():
            return request.redirect('/contacts')

        can_edit = request.env.user.has_group('base.group_user')

        return request.render("ak_library_management.contact_detail", {
            'partner': partner,
            'can_edit': can_edit
        })

    @http.route('/contacts/update', type='json', auth="user", website=True)
    def update_contact(self, **kwargs):
        """
        Update contact information via AJAX.
        """
        partner_id = kwargs.get('partner_id')
        if not partner_id:
            return {'success': False, 'error': 'Partner ID is required'}

        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return {'success': False, 'error': 'Contact not found'}

        if not request.env.user.has_group('base.group_user'):
            return {'success': False, 'error': 'You do not have permission to edit contacts'}

        # Validation checks
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')

        if not name:
            return {'success': False, 'error': 'Name is required'}
        if not email:
            return {'success': False, 'error': 'email is required'}
        if not phone:
            return {'success': False, 'error': 'phone is required'}
        if email:
            # Check for duplicate email
            duplicate = request.env['res.partner'].sudo().search([
                ('email', '=', email),
                ('id', '!=', partner.id)
            ], limit=1)

            if duplicate:
                return {'success': False, 'error': 'Email already exists'}

        update_values = {
            'name': name,
            'email': email,
            'phone': phone,
            'mobile': kwargs.get('mobile'),
            'function': kwargs.get('function'),
            'website': kwargs.get('website'),
            'vat': kwargs.get('vat')
        }
        try:
            partner.sudo().write(update_values)
            return {
                'success': True,
                'message': 'Contact updated successfully',
                'data': {
                    'partner_id': partner.id,
                    'name': partner.name,
                    'email': partner.email,
                    'phone': partner.phone,
                    'mobile': partner.mobile,
                    'function': partner.function,
                    'website': partner.website,
                    'vat': partner.vat,
                    'company_name': partner.company_id.name
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

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

class ProductImagesDownload(http.Controller):

    @http.route(['/download_images/<model("product.template"):product>'], type='http', auth="public", website=True)
    def download_product_images(self, product, **kw):
        # Collect all product images
        images = []
        # Helper function to detect image format
        def get_image_format(image_data):
            # Check first few bytes for file signature
            if image_data.startswith(b'\xFF\xD8\xFF'):
                return 'jpg'
            elif image_data.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'png'
            elif image_data.startswith(b'GIF87a') or image_data.startswith(b'GIF89a'):
                return 'gif'
            elif image_data.startswith(b'RIFF') and image_data[8:12] == b'WEBP':
                return 'webp'
            else:
                return 'jpg'  # Default to JPG if unknown
        # Add main product image if it exists
        if product.image_1920:
            image_data = base64.b64decode(product.image_1920)
            format = get_image_format(image_data)

            images.append({
                'name': f"{product.name}_main.{format}",
                'data': image_data,
                'format': format
            })
        # Add extra product images (from eCommerce Media section)
        for idx, img in enumerate(product.product_template_image_ids):
            image_data = base64.b64decode(img.image_1920)
            format = get_image_format(image_data)

            images.append({
                'name': f"{product.name}_image_{idx + 1}.{format}",
                'data': image_data,
                'format': format
            })
        # Handle cases with no images
        if not images:
            return request.redirect('/shop')
        # If only one image, download directly
        if len(images) == 1:
            img = images[0]
            mime_type = f"image/{img['format']}"

            return http.request.make_response(
                img['data'],
                headers=[
                    ('Content-Type', mime_type),
                    ('Content-Disposition', f'attachment; filename="{img["name"]}"'),
                    ('Content-Length', len(img['data'])),
                ]
            )
        # If multiple images, create a zip
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for img in images:
                zf.writestr(img['name'], img['data'])

        memory_file.seek(0)
        zip_data = memory_file.read()

        return http.request.make_response(
            zip_data,
            headers=[
                ('Content-Type', 'application/zip'),
                ('Content-Disposition', f'attachment; filename="{product.name}_images.zip"'),
                ('Content-Length', len(zip_data)),
            ]
        )

