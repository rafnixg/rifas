# -*- coding: utf-8 -*-
"""
Main home controller for the Rifas module.

This module handles the main routes and views for displaying available
raffles on the public website.
"""

from odoo import http
from odoo.http import request
import json


class RifaController(http.Controller):
    """
    Main controller for managing the raffle home page.
    
    This controller handles the display of available raffles on the website
    and provides the main interface for public users.
    """

    @http.route("/", type="http", auth="public", website=True)
    def index(self, **kwargs):
        """
        Render the main page of the raffle module.
        
        Displays all raffles that are in 'publish' state along with
        available payment methods.
        
        Args:
            **kwargs: Additional URL arguments
            
        Returns:
            Response: Rendered page with raffles and available payment methods
            
        Note:
            - Only shows raffles in 'publish' state
            - Includes all configured payment methods
            - Publicly accessible without authentication
        """
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
