odoo.define('rifas.checkout', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.CheckoutPage = publicWidget.Widget.extend({
        selector: '.checkout-container',
        events: {
            'change #payment_method': '_onChangePaymentMethod',
        },
        
        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);
            return def;
        },
        
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        
        /**
         * Show/hide payment method details when a payment method is selected
         *
         * @private
         * @param {Event} ev
         */
        _onChangePaymentMethod: function (ev) {
            var $target = $(ev.currentTarget);
            var methodId = $target.val();
            
            // Hide all payment method details
            $('.payment-method-details').hide();
            
            // Show the details for the selected payment method
            if (methodId) {
                $('#payment-info-' + methodId).show();
            }
        },
    });
    
    return publicWidget.registry.CheckoutPage;
});