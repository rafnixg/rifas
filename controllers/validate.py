from odoo import http
from odoo.http import request
from ..models.sale_order import STATE_SALE_ORDER

class SaleOrderValidationController(http.Controller):

    def _get_state_sale_order(self, state):
        """
        STATE_SALE_ORDER is a list of tuples that contains the state of the sale order.
        This method returns the state of the sale order.
        """
        for state_tuple in STATE_SALE_ORDER:
            if state_tuple[0] == state:
                return state_tuple[1]
        return "Desconocido"
        

    @http.route(["/rifas/validate"], type="http", auth="public", website=True)
    def validate_sale_order(self, **kwargs):
        """
        This method is triggered when the user clicks on the validation link in the email.
        It renders the sale order validation confirmation page.
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
