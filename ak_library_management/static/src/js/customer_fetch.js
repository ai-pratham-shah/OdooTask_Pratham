/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CustomerPage = publicWidget.Widget.extend({
    selector: '.customers_page',
    events: {
        'click #fetchCustomer': '_onFetchCustomer'
    },

    _onFetchCustomer: function () {
        var email = $('#InputEmail').val().trim();
        if (!email) {
            alert("Please enter an email address.");
            return;
        }
        rpc('/customer_page/get_customer', { email: email }).then(function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                $('#InputName').val(data.name);
                $('#InputPhone').val(data.phone);
            }
        }).catch(function (error) {
            console.error("Error fetching customer details:", error);
            alert("Failed to fetch customer details.");
        });
    }
});
