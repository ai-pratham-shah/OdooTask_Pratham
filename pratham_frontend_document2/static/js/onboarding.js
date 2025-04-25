/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.OnboardingForm = publicWidget.Widget.extend({
    selector: '.onboarding-form',

    start: function() {
        console.log("OnboardingForm widget starting...");
        const result = this._super.apply(this, arguments);
        // Initialize form validation
        this._initFormValidation();
        console.log("OnboardingForm widget initialized successfully");
        return result;
    },

    events: {
        'input #mobile_number': '_validateMobileNumber',
        'input #passport_number': '_validatePassportNumber',
        'submit form': '_validateForm'
    },

    /**
     * Initialize form validation
     * @private
     */
    _initFormValidation: function() {
        // Add any additional initialization logic here
        this._validateMobileNumber();
        this._validatePassportNumber();
    },

    /**
     * Validate Indian mobile number format
     * @private
     */
    _validateMobileNumber: function() {
        console.log("Validating mobile number");
        const $input = this.$('#mobile_number');
        const value = $input.val();
        const isValid = /^\+91[0-9]{10}$/.test(value);

        if (value) {
            if (isValid) {
                $input.removeClass('input-error').addClass('input-valid');
                $input.siblings('.text-danger').hide();
            } else {
                $input.removeClass('input-valid').addClass('input-error');
                $input.siblings('.text-danger').show();
            }
        } else {
            $input.removeClass('input-error').removeClass('input-valid');
            $input.siblings('.text-danger').hide();
        }

        return isValid;
    },

    /**
     * Validate passport number format (16-digit integer)
     * @private
     */
    _validatePassportNumber: function() {
        console.log("Validating passport number");
        const $input = this.$('#passport_number');
        const value = $input.val();
        const isValid = /^[0-9]{16}$/.test(value);

        if (value) {
            if (isValid) {
                $input.removeClass('input-error').addClass('input-valid');
                $input.siblings('.text-danger').hide();
            } else {
                $input.removeClass('input-valid').addClass('input-error');
                $input.siblings('.text-danger').show();
            }
        } else {
            $input.removeClass('input-error').removeClass('input-valid');
            $input.siblings('.text-danger').hide();
        }

        return isValid;
    },

    /**
     * Validate the entire form before submission
     * @private
     * @param {Event} event
     */
    _validateForm: function(event) {
        console.log("Form submission attempted");
        event.preventDefault();

        const isMobileValid = this._validateMobileNumber();
        const isPassportValid = this._validatePassportNumber();

        if (!isMobileValid || !isPassportValid) {
            // Show error message
            this._showFormError();
            console.log("Form validation failed");
            return;
        }

        console.log("Form validation passed, submitting via RPC");
        this._submitFormViaRPC();
    },

    /**
     * Submit form data using RPC
     * @private
     */
    _submitFormViaRPC: function() {
        // Collect form data
        const formData = {
            date_of_birth: $('#date_of_birth').val(),
            place_of_birth: $('#place_of_birth').val(),
            gender: $('#gender').val(),
            mobile_number: $('#mobile_number').val(),
            passport_number: $('#passport_number').val(),
            driving_license: $('#driving_license').val(),
            speaking_language: $('input[name="speaking_language"]:checked').val(),
            marital_status: $('#marital_status').val(),
            job_position: $('#job_position').val(),
            address: $('#address').val().trim()
        };

        console.log("Sending RPC request with data:", formData);

        // Hide any previous messages
        $('.form-error-message, .form-success-message').hide();

        // Send RPC request
        rpc('/onboarding/submit_ajax', formData)
            .then((result) => {
                console.log("RPC response:", result);
                if (result.success) {
                    // Show success message
                    this._showSuccessMessage(result.message);

                    // Redirect to success page after delay
                    setTimeout(() => {
                        window.location.href = '/onboarding/success';
                    }, 2000);
                } else {
                    // Show error message
                    this._showFormError(result.error || 'An error occurred while processing your information.');
                }
            })
            .catch((error) => {
                console.error("RPC error:", error);
                this._showFormError('An error occurred while submitting the form. Please try again.');
            });
    },

    /**
     * Show form error message
     * @private
     * @param {String} message - Optional custom error message
     */
    _showFormError: function(message) {
        console.log("Showing form error message");
        const errorText = message || 'Please correct the errors in the form before submitting.';
        const $errorMsg = this.$('.form-error-message');

        if ($errorMsg.length === 0) {
            this.$('form').prepend(`<div class="alert alert-danger form-error-message">${errorText}</div>`);
        } else {
            $errorMsg.text(errorText).show();
        }
    },

    /**
     * Show success message
     * @private
     * @param {String} message - Success message to display
     */
    _showSuccessMessage: function(message) {
        console.log("Showing success message");
        const successText = message || 'Form submitted successfully!';
        const $successMsg = this.$('.form-success-message');

        if ($successMsg.length === 0) {
            this.$('form').prepend(`<div class="alert alert-success form-success-message">${successText}</div>`);
        } else {
            $successMsg.text(successText).show();
        }
    }
});