// Vanilla JS implementation for raffle ticket selection
document.addEventListener('DOMContentLoaded', function() {
    // Initialize ticket selection functionality
    initTicketSelection();
});

function initTicketSelection() {
    const ticketSelector = document.querySelector('.ticket-selector');
    
    // If we're not on the raffle page, exit
    if (!ticketSelector) {
        return;
    }
    
    const ticketPrice = parseFloat(ticketSelector.dataset.price) || 0;
    const raffleId = ticketSelector.dataset.raffleId;
    const selectedTickets = [];
    
    // Add click handlers to all ticket numbers
    const ticketButtons = document.querySelectorAll('.ticket-selector__number');
    ticketButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const number = this.dataset.number;
            
            // Toggle selection
            if (this.classList.contains('selected')) {
                // Remove selection
                this.classList.remove('selected');
                
                // Remove from selectedTickets array
                const index = selectedTickets.findIndex(t => t.number === number);
                if (index !== -1) {
                    selectedTickets.splice(index, 1);
                }
            } else {
                // Add selection
                this.classList.add('selected');
                
                // Add to selectedTickets array
                selectedTickets.push({
                    number
                });
            }
            
            // Update summary
            updateSummary();
        });
    });
    
    // Checkout button handler
    const checkoutButton = ticketSelector.querySelector('.button-checkout');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (selectedTickets.length === 0) {
                return;
            }
            // Create comma-separated list of IDs
            const ticketIds = selectedTickets.map(t => t.number).join(',');
            
            // Redirect to checkout page
            window.location.href = '/rifas/checkout/' + raffleId + '?ticket_ids=' + ticketIds;
        });
    }
    
    // Function to update the summary display
    function updateSummary() {
        const count = selectedTickets.length;
        const total = (count * ticketPrice).toFixed(2);
        
        document.getElementById('ticket-count').textContent = count;
        document.getElementById('ticket-total').textContent = total;
        
        // Enable/disable checkout button based on selection
        if (count > 0) {
            checkoutButton.removeAttribute('disabled');
        } else {
            checkoutButton.setAttribute('disabled', 'disabled');
        }
    }
    
    // Initialize summary
    updateSummary();
}