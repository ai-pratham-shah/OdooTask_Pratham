/* @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
import { cartHandlerMixin } from '@website_sale/js/website_sale_utils';
import { WebsiteSale } from '@website_sale/js/website_sale';

publicWidget.registry.ShopPageQuickAddToCart = WebsiteSale.extend(cartHandlerMixin, {
   selector: '.oe_website_sale',
   events: {
       'click .quick_add_to_cart': '_onClickQuickAddToCart',
   },
   /**
    * Handles click on "Add to Cart" button in shop page
    * @param {Event} ev
    */
   _onClickQuickAddToCart: async function (ev) {
       ev.preventDefault();
       ev.stopPropagation();
       const $btn = $(ev.currentTarget);
       // Make sure getting the correct product ID from the clicked button
       const productId = parseInt($btn.data('product-id'));
        if (!productId) {
           console.error("Product ID not found on button");
           this.notification.add(
               _t('Could not identify product'),
               { title: _t('Error'), type: 'danger' }
           );
           return;
       }
       // Add to cart using the cartHandlerMixin - passing exact product ID
       this.stayOnPageOption = true;
       const result = await this.addToCart({
            product_id: productId,
            add_qty: 1,
       });
   },
});

export default publicWidget.registry.ShopPageQuickAddToCart;
