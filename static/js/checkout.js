// Vanilla JS implementation for checkout page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize checkout page functionality
    initCheckoutPage();
});

function initCheckoutPage() {
    const checkoutContainer = document.querySelector('.checkout-container');
    
    // If we're not on the checkout page, exit
    if (!checkoutContainer) {
        return;
    }
    
    // Payment method selection handler
    const paymentMethodSelect = document.getElementById('payment_method');
    if (paymentMethodSelect) {
        paymentMethodSelect.addEventListener('change', function() {
            const methodId = this.value;
            
            // Hide all payment method details
            const methodDetails = document.querySelectorAll('.payment-method-details');
            methodDetails.forEach(function(detail) {
                detail.style.display = 'none';
            });
            
            // Show the details for the selected payment method
            if (methodId) {
                const selectedDetail = document.getElementById('payment-info-' + methodId);
                if (selectedDetail) {
                    selectedDetail.style.display = 'block';
                }
            }
        });
    }
}