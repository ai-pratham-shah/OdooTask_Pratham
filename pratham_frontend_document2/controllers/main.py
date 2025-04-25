import re
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError


class OnboardingController(http.Controller):

    def _check_onboarding_enabled(self):
        """Check if onboarding is enabled in settings"""
        return request.env['ir.config_parameter'].sudo().get_param('pratham_frontend_document2.enable_user_onboarding',
                                                                   'False').lower() == 'true'

    def _get_onboarding_status(self, user):
        """Check if user has completed onboarding"""
        return user.onboarding_completed

    @http.route('/onboarding/welcome', type='http', auth='user', website=True)
    def onboarding_welcome(self, **kw):
        """Display welcome page for onboarding"""
        if not self._check_onboarding_enabled():
            return request.redirect('/web')

        user = request.env.user
        if self._get_onboarding_status(user):
            return request.redirect('/web')

        return request.render('pratham_frontend_document2.onboarding_welcome_template', {
            'user': user,
        })

    @http.route('/onboarding/details', type='http', auth='user', website=True)
    def onboarding_details(self, **kw):
        """Display details form for onboarding"""
        if not self._check_onboarding_enabled():
            return request.redirect('/web')

        user = request.env.user
        if self._get_onboarding_status(user):
            return request.redirect('/web')

        return request.render('pratham_frontend_document2.onboarding_details_template', {
            'user': user,
        })

    @http.route('/onboarding/submit', type='http', auth='user', website=True, methods=['POST'])
    def onboarding_submit(self, **post):
        """Process submitted onboarding form"""
        if not self._check_onboarding_enabled():
            return request.redirect('/web')

        user = request.env.user
        if self._get_onboarding_status(user):
            return request.redirect('/web')

        # Validate inputs
        errors = {}

        # Mobile number validation for Indian numbers (+91)
        mobile = post.get('mobile_number', '')
        if mobile and not re.match(r'^\+91[0-9]{10}$', mobile):
            errors['mobile_number'] = _("Please enter a valid Indian mobile number (+91XXXXXXXXXX)")

        # Passport validation (16-digit integer)
        passport = post.get('passport_number', '')
        if passport and (not passport.isdigit() or len(passport) != 16):
            errors['passport_number'] = _("Passport number must be a 16-digit number")

        # Re-render the form if there are validation errors
        if errors:
            return request.render('pratham_frontend_document2.onboarding_details_template', {
                'user': user,
                'errors': errors,
                'post': post,
            })

        # Update user information
        vals = {
            'date_of_birth': post.get('date_of_birth'),
            'place_of_birth': post.get('place_of_birth'),
            'gender': post.get('gender'),
            'mobile_number': post.get('mobile_number'),
            'passport_number': post.get('passport_number'),
            'driving_license': post.get('driving_license'),
            'speaking_language': post.get('speaking_language'),
            'marital_status': post.get('marital_status'),
            'job_position': post.get('job_position'),
            'onboarding_completed': True,
        }

        user.sudo().write(vals)

        # Send email notification
        template = request.env.ref('pratham_frontend_document2.mail_template_onboarding_complete')
        if template:
            template.sudo().send_mail(user.id, force_send=True)

        return request.redirect('/onboarding/success')

    @http.route('/onboarding/success', type='http', auth='user', website=True)
    def onboarding_success(self, **kw):
        """Display success page after onboarding completion"""
        if not self._check_onboarding_enabled():
            return request.redirect('/web')

        user = request.env.user

        return request.render('pratham_frontend_document2.onboarding_success_template', {
            'user': user,
        })


class HomeInherit(Home):
    @http.route()
    def web_login(self, redirect=None, **kw):
        """Override login to check if onboarding is needed"""
        response = super(HomeInherit, self).web_login(redirect=redirect, **kw)

        if not request.httprequest.method == 'POST':
            return response

        if not request.session.uid:
            return response

        # Check if onboarding is enabled in settings
        onboarding_enabled = request.env['ir.config_parameter'].sudo().get_param(
            'pratham_frontend_document2.enable_user_onboarding', 'False').lower() == 'true'

        if not onboarding_enabled:
            return response

        # Check if user has completed onboarding
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user and not user.onboarding_completed:
            return request.redirect('/onboarding/welcome')

        return response


class CustomerPortalInherit(CustomerPortal):
    @http.route(['/my', '/my/home'], type='http', auth='user', website=True)
    def home(self, **kw):
        """Override portal home to check if onboarding is needed"""
        # Check if onboarding is enabled in settings
        onboarding_enabled = request.env['ir.config_parameter'].sudo().get_param(
            'pratham_frontend_document2.enable_user_onboarding', 'False').lower() == 'true'

        if onboarding_enabled:
            # Check if user has completed onboarding
            user = request.env.user
            if not user.onboarding_completed:
                return request.redirect('/onboarding/welcome')

        return super(CustomerPortalInherit, self).home(**kw)