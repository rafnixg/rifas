# -*- coding: utf-8 -*-
"""
Sale Order Validation Controller for Rifas Module.

This module handles the validation of sale orders through email confirmation links
and provides web endpoints for order validation status display.
"""
from odoo import http
from odoo.http import request
from ..models.sale_order import STATE_SALE_ORDER


class SaleOrderValidationController(http.Controller):
    """
    Controller for handling sale order validation through email confirmation.
    
    This controller provides endpoints for validating sale orders via unique
    validation codes sent through email confirmation links.
    """

    def _get_state_sale_order(self, state):
        """
        Get the human-readable description of a sale order state.
        
        Converts internal sale order state codes to user-friendly descriptions
        by looking up the state in the STATE_SALE_ORDER configuration.
        
        Args:
            state (str): The internal state code of the sale order
            
        Returns:
            str: Human-readable description of the state, or "Desconocido" 
                 (Unknown) if state is not found
                 
        Note:
            Uses the STATE_SALE_ORDER constant which contains tuples of
            (internal_code, display_name) for all possible order states.
        """
        for state_tuple in STATE_SALE_ORDER:
            if state_tuple[0] == state:
                return state_tuple[1]
        return "Desconocido"

    @http.route(["/rifas/validate"], type="http", auth="public", website=True)
    def validate_sale_order(self, **kwargs):
        """
        Handle sale order validation through email confirmation links.
        
        This endpoint is accessed when users click on validation links sent via email.
        It validates the provided validation code and renders the appropriate
        confirmation page with order details or error messages.
        
        Args:
            **kwargs: Request parameters including:
                - validation_code (str): Unique validation code for the sale order
                
        Returns:
            Response: Rendered template with validation results:
                - Success: Shows order details and current state
                - Error: Shows appropriate error message for invalid/missing codes
                
        Note:
            - Publicly accessible endpoint (no authentication required)
            - Uses sudo() to access sale order records
            - Handles missing or invalid validation codes gracefully
        """
        validation_code = kwargs.get("validation_code")
        sale_order = None
        error = None
        if not validation_code:
            return request.render(
                "rifas.sale_order_form_validation_confirmation", {"error": "None"}
            )

        sale_order = (
            request.env["rifas.sale_order"]
            .sudo()
            .search([("validation_code", "=", validation_code)], limit=1)
        )
        if not sale_order:
            return request.render(
                "rifas.sale_order_form_validation_confirmation",
                {"error": "No existe una orden de venta con ese código de validación."},
            )
        
        return request.render(
            "rifas.sale_order_validation_confirmation",
            {
                "order": sale_order,
                "error": error,
                "state": self._get_state_sale_order(sale_order.state),
            },
        )