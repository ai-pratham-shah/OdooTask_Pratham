/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ContactPage = publicWidget.Widget.extend({
    selector: '.contact_page',

    start: function() {
        console.log("ContactPage widget starting...");
        const result = this._super.apply(this, arguments);
        console.log("ContactPage widget initialized successfully");
        return result;
    },

    events: {
        'click #btn-edit': '_onEditClick',
        'click #btn-cancel': '_onCancelClick',
        'click #btn-save': '_onSaveClick'
    },

    _onEditClick: function(event) {
        console.log("Edit button clicked");
        $('.edit-mode').removeClass('d-none');
        $('[id$="-display"]').addClass('d-none');
        $('#btn-save, #btn-cancel').removeClass('d-none');
        $('#btn-edit').addClass('d-none');
    },

    _onCancelClick: function(event) {
        console.log("Cancel button clicked");
        $('.edit-mode').addClass('d-none');
        $('[id$="-display"]').removeClass('d-none');
        $('.is-invalid').removeClass('is-invalid');
        $('#error-message').addClass('d-none').text('');
        $('#btn-edit').removeClass('d-none');
        $('#btn-save, #btn-cancel').addClass('d-none');
    },

    _formatPhoneNumber: function(phoneNumber) {
        // Remove all non-digit characters
        const digitsOnly = phoneNumber.replace(/\D/g, '');
        // Check if we have exactly 10 digits
        if (digitsOnly.length === 10) {
            return `(${digitsOnly.slice(0, 3)})-${digitsOnly.slice(3, 6)}-${digitsOnly.slice(6, 10)}`;
        }
        // Return original input if not 10 digits
        return phoneNumber;
    },

    _validatePhoneNumber: function(phoneNumber) {
        if (!phoneNumber) return true;
        // Check if it's already in the format (XXX)-XXX-XXXX
        if (/^\(\d{3}\)-\d{3}-\d{4}$/.test(phoneNumber)) {
            return true;
        }
        // Check if it has exactly 10 digits when non-digits are removed
        const digitsOnly = phoneNumber.replace(/\D/g, '');
        return digitsOnly.length === 10;
    },

    _onSaveClick: function(event) {
        console.log("Save button clicked");
        $('.is-invalid').removeClass('is-invalid');
        $('#error-message, #success-message').addClass('d-none').text('');

        let isValid = true;
        const name = $('#input-name').val().trim();
        if (!name) {
            $('#input-name').addClass('is-invalid');
            isValid = false;
        }

        const email = $('#input-email').val().trim();
        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            $('#input-email').addClass('is-invalid');
            isValid = false;
        }

        const phone = $('#input-phone').val().trim();
        if (phone && !this._validatePhoneNumber(phone)) {
            $('#input-phone').addClass('is-invalid');
            isValid = false;
        }

        const mobile = $('#input-mobile').val().trim();
        if (mobile && !/^[+]?[\d\s()-]{10,10}$/.test(mobile)) {
            $('#input-mobile').addClass('is-invalid');
            isValid = false;
        }

        if (!isValid) {
            $('#error-message').removeClass('d-none').text('Please correct the errors in the form.');
            return;
        }

        const formattedPhone = phone ? this._formatPhoneNumber(phone) : phone;

        const data = {
            partner_id: $('#partner-id').val(),
            name: name,
            email: email,
            phone: formattedPhone,
            mobile: mobile,
        };

        console.log("Sending RPC request with data:", data);

        rpc('/contacts/update', data)
            .then((result) => {
                console.log("RPC response:", result);
                if (result.success) {
                    $('#contact-name-display').text(result.data.name);
                    $('#email-display').text(result.data.email || 'N/A');
                    $('#phone-display').text(result.data.phone || 'N/A');
                    $('#mobile-display').text(result.data.mobile || 'N/A');
                    $('.edit-mode').addClass('d-none');
                    $('[id$="-display"]').removeClass('d-none');
                    $('#btn-edit').removeClass('d-none');
                    $('#btn-save, #btn-cancel').addClass('d-none');

                    $('#success-message').removeClass('d-none').text(result.message);
                    setTimeout(() => {
                        $('#success-message').addClass('d-none');
                    }, 3000);
                } else {
                    $('#error-message').removeClass('d-none').text(result.error);
                }
            })
            .catch((error) => {
                console.error("RPC error:", error);
                $('#error-message').removeClass('d-none').text('An error occurred while saving. Please try again.');
            });
    },
});
