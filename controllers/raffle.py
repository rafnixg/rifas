# -*- coding: utf-8 -*-
"""
Controller for individual raffle visualization.

This module handles the detailed view of each specific raffle,
including information about available and sold tickets.
"""

from odoo import http
from odoo.http import request


class RaffleController(http.Controller):
    """
    Controller for managing individual raffle views.
    
    This controller handles the detailed visualization of specific raffles,
    calculating available tickets and providing complete information
    for ticket purchases.
    """

    @http.route("/rifas/<slug>", type="http", auth="public", website=True)
    def view_raffle(self, slug, **kwargs):
        """
        Display the detailed view of a specific raffle.
        
        Searches for a raffle by its unique slug and displays detailed information
        including available tickets, sold tickets, and payment methods.
        
        Args:
            slug (str): Unique identifier of the raffle (slug)
            **kwargs: Additional URL arguments
            
        Returns:
            Response: Detailed raffle page or 404 error if not found
            
        Note:
            - Automatically calculates available vs sold tickets
            - Includes active payment methods
            - Generates list of available tickets with prices
            - Publicly accessible without authentication
            
        Raises:
            NotFound: If the raffle with the specified slug doesn't exist
        """
        # Buscar la rifa por su slug
        rifa = request.env["rifas.raffle"].sudo().search([("slug", "=", slug)], limit=1)
        # Verificar si la rifa existe
        if not rifa.exists():
            return request.not_found()

        # Obtener números de boletos ya vendidos
        tickets_sold = rifa.ticket_ids.mapped("number")
        tickets_sold = [int(ticket) for ticket in tickets_sold]
        
        # Generar lista de todos los boletos posibles
        tickets_totales = list(range(1, rifa.ticket_max))
        
        # Calcular boletos disponibles (no vendidos)
        tickets_disp = list(set(tickets_totales) - set(tickets_sold))
        
        # Crear diccionario con información de boletos disponibles
        tickets_disponibles_dict = [
            {
                "number": number,
                "price": rifa.price,
            }
            for number in tickets_disp
        ]
        
        # Renderizar la vista con la plantilla y los datos de la rifa
        return request.render(
            "rifas.raffle_template",
            {
                "rifa": rifa,
                "payments_method": request.env["rifas.payment_method"]
                .sudo()
                .search([]),
                "tickets_disponibles": tickets_disponibles_dict,
            },
        )
