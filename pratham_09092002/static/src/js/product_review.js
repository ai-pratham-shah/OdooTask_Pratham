/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ProductReviewForm = publicWidget.Widget.extend({
    selector: '.review-form-container',
    events: {
        'click .rating-stars label': '_onStarClick',
        'submit .review-form': '_onFormSubmit'
    },

    /**
     * Handle star rating click
     */
    _onStarClick: function (event) {
        const $target = $(event.currentTarget);
        const $stars = $target.siblings('label').addBack();
        const $input = $target.prev('input');
        const value = $input.val();

        // Visual feedback for star selection
        $stars.removeClass('selected');
        $stars.each(function () {
            const $this = $(this);
            if ($this.prev('input').val() <= value) {
                $this.addClass('selected');
            }
        });
    },

    /**
     * Form validation before submit
     */
    _onFormSubmit: function (event) {
         event.preventDefault();
         rpc('/shop/product/submit_review', {
             product_id: $form.find('input[name="product_id"]').val(),
             rating: $rating.val(),
             description: $description.val().trim()
         }).then(function (result) {
             window.location.reload();
         }).catch(function (error) {
             console.error("Error submitting review:", error);
             this._showError("Failed to submit review.");
         });
    },

    /**
     * Display error message
     */
    _showError: function (message) {
        $('.review-form .alert').remove();
        const $error = $('<div class="alert alert-danger mt8">' + message + '</div>');
        $('.review-form').prepend($error);
        setTimeout(function () {
            $error.fadeOut(function () {
                $error.remove();
            });
        }, 4000);
    }
});