from odoo import http
from odoo.http import request
import json


class RifaController(http.Controller):

    @http.route("/", type="http", auth="public", website=True)
    def index(self, **kwargs):
        # Obtener las rifas en estado 'publish'
        rifas = request.env["rifas.raffle"].sudo().search([("state", "=", "publish")])
        payments_method = request.env["rifas.payment_method"].sudo().search([])

        return request.render(
            "rifas.rifas_index",
            {
                "rifas": rifas,
                "payments_method": payments_method,
            },
        )
