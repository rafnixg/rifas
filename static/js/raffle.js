odoo.define('rifas.raffle', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.RafflePage = publicWidget.Widget.extend({
        selector: '.ticket-selector',
        events: {
            'click .ticket-selector__number': '_onClickTicket',
            'click .button-checkout': '_onClickCheckout',
        },
        
        /**
         * @override
         */
        start: function () {
            this.selectedTickets = [];
            this.ticketPrice = parseFloat($('.ticket-selector').data('price')) || 0;
            this._updateSummary();
            return this._super.apply(this, arguments);
        },
        
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
        
        /**
         * Updates the summary with the current selection
         *
         * @private
         */
        _updateSummary: function () {
            var count = this.selectedTickets.length;
            var total = (count * this.ticketPrice).toFixed(2);
            
            $('#ticket-count').text(count);
            $('#ticket-total').text(total);
            
            // Enable/disable checkout button based on selection
            if (count > 0) {
                $('.button-checkout').removeAttr('disabled');
            } else {
                $('.button-checkout').attr('disabled', 'disabled');
            }
        },
        
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        
        /**
         * Handles click on a ticket number
         *
         * @private
         * @param {Event} ev
         */
        _onClickTicket: function (ev) {
            var $ticket = $(ev.currentTarget);
            var ticketNumber = $ticket.data('number');
            var ticketId = $ticket.data('id');
            
            // Toggle selection
            if ($ticket.hasClass('selected')) {
                // Remove from selection
                $ticket.removeClass('selected');
                this.selectedTickets = this.selectedTickets.filter(function(t) {
                    return t.id !== ticketId;
                });
            } else {
                // Add to selection
                $ticket.addClass('selected');
                this.selectedTickets.push({
                    id: ticketId,
                    number: ticketNumber
                });
            }
            
            this._updateSummary();
        },
        
        /**
         * Handles click on the checkout button
         *
         * @private
         * @param {Event} ev
         */
        _onClickCheckout: function (ev) {
            ev.preventDefault();
            
            if (this.selectedTickets.length === 0) {
                return;
            }
            
            var raffleId = $('.ticket-selector').data('raffle-id');
            var ticketIds = this.selectedTickets.map(function(t) { return t.id; }).join(',');
            
            // Redirect to checkout page
            window.location.href = '/rifas/checkout/' + raffleId + '?ticket_ids=' + ticketIds;
        }
    });
    
    return publicWidget.registry.RafflePage;
});