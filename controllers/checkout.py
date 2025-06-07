# -*- coding: utf-8 -*-
"""
Checkout controller for raffle ticket purchases.

This module handles the complete checkout process for raffle tickets,
including validation, payment processing, and order confirmation.
"""
import base64

from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError


class RifasCheckout(http.Controller):
    """
    Controller for managing the raffle ticket checkout process.
    
    This controller handles the complete checkout workflow including:
    - Ticket availability validation
        - Customer information collection
    - Payment processing
    - Order creation and confirmation
    - Email notifications
    """
    
    def _validate_ticket_availability(self, raffle_id, ticket_ids):
        """
        Validate if the selected tickets are available for purchase.
        
        Checks if any of the selected tickets have already been sold for the specified raffle.
        
        Args:
            raffle_id (int): The ID of the raffle to check tickets for
            ticket_ids (list): List of dictionaries containing ticket information with 'number' key
            
        Raises:
            ValidationError: If any of the selected tickets are already sold/unavailable
            
        Note:
            This method ensures data integrity by preventing double-booking of tickets
        """
        ticket_ids_list = [ticket_id["number"] for ticket_id in ticket_ids]
        tickets = (
            request.env["rifas.ticket"]
            .sudo()
            .search([("number", "in", ticket_ids_list), ("rifa_id", "=", raffle_id)])
        )
        if tickets:
            raise ValidationError(_("Some selected tickets are not available."))
    
    def _get_selected_tickets(self, raffle, post):
        """
        Retrieve selected tickets from the session or post data.
        
        Processes the ticket_ids from POST data and validates their availability
        for the specified raffle.
        
        Args:
            raffle (rifas.raffle): The raffle record object
            post (dict): POST data containing ticket_ids as comma-separated string
            
        Returns:
            list: List of dictionaries containing ticket information with keys:
                - number (int): Ticket number
                - raffle_id (int): ID of the raffle
                - price (float): Price per ticket
                - raffle_name (str): Name of the raffle
            or
            redirect: Redirect response if no tickets selected
            
        Note:
            Automatically validates ticket availability and redirects to raffle page
            if no valid tickets are selected
        """
        ticket_ids = post.get("ticket_ids", [])
        selected_tickets = [
            {
                "number": int(x),
                "raffle_id": raffle.id,
                "price": raffle.price,
                "raffle_name": raffle.name,
            }
            for x in ticket_ids.split(",")
            if x.isdigit()
        ]

        if not selected_tickets:
            # No tickets selected, redirect to raffle page
            return request.redirect(f"/raffle/{raffle.id}")
        self._validate_ticket_availability(raffle.id, selected_tickets)
        return selected_tickets

    @http.route(
        ["/rifas/checkout/<int:raffle_id>"], type="http", auth="public", website=True
    )
    def checkout(self, raffle_id, **post):
        """Display the checkout page with selected tickets"""
        raffle = request.env["rifas.raffle"].sudo().browse(raffle_id)
        if not raffle.exists():
            return request.redirect("/")

        # Get selected tickets from session or post
        selected_tickets = self._get_selected_tickets(raffle, post)
        if not selected_tickets:
            return request.redirect(f"/raffle/{raffle_id}")

        payment_methods = (
            request.env["rifas.payment_method"]
            .sudo()
            .search([("is_active", "=", True)])
        )

        total_amount = len(selected_tickets) * raffle.price

        values = {
            "raffle": raffle,
            "selected_tickets": selected_tickets,
            "total_amount": total_amount,
            "payment_methods": payment_methods,
        }

        return request.render("rifas.rifas_checkout", values)

    @http.route(
        ["/rifas/checkout/submit/<int:raffle_id>"],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def checkout_submit(self, raffle_id, **post):
        """Process the checkout form submission"""
        raffle = request.env["rifas.raffle"].sudo().browse(raffle_id)
        if not raffle.exists():
            return request.redirect("/rifas")

        # Get payment_image from post data
        payment_image = request.httprequest.files.get("payment_image")
            
        # Get selected tickets from post data
        selected_tickets = self._get_selected_tickets(raffle, post)
        if not selected_tickets:
            return request.redirect(f"/raffle/{raffle_id}")

        # Create or update client
        client_values = {
            "name": post.get("name"),
            "email": post.get("email"),
            "phone": post.get("phone"),
            # 'street': post.get('address'),
            # 'vat': post.get('document'),
        }

        # Find existing client by email
        client = (
            request.env["rifas.client"]
            .sudo()
            .search([("email", "=", post.get("email"))], limit=1)
        )

        if client:
            # Update existing client
            client.sudo().write(client_values)
        else:
            # Create new client
            client = request.env["rifas.client"].sudo().create(client_values)

        # Calculate total amount
        total_amount = len(selected_tickets) * raffle.price

        # Create the sale order
        order_values = {
            "client_id": client.id,
            "rifa_id": raffle.id,
            "amount": total_amount,
            # 'payment_method_id': int(post.get('payment_method')) if post.get('payment_method') else False,
            # 'payment_reference': post.get('payment_reference', ''),
            # 'notes': post.get('payment_notes', ''),
        }

        order = request.env["rifas.sale_order"].sudo().create(order_values)

        # Link tickets to the order and mark them as reserved
        tickets = [
            {
                "number": ticket["number"],
                "rifa_id": raffle.id,
                "sale_order_id": order.id,
                "client_id": client.id,
            }
            for ticket in selected_tickets
        ]
        request.env["rifas.ticket"].sudo().create(tickets)

        # Create payment record
        payment_values = {
            "client_id": client.id,
            "rifa_id": raffle.id,
            "sale_order_id": order.id,
            "amount": total_amount,
            "payment_method_id": (
                int(post.get("payment_method")) if post.get("payment_method") else False
            ),
            "reference": post.get("payment_reference", ""),
            "reference_image": base64.b64encode(payment_image.read())	
            # 'notes': post.get('payment_notes', ''),
        }
        payment = request.env["rifas.payment"].sudo().create(payment_values)

        order.payment_id = payment.id
        order.ticket_ids.write({"payment_id": payment.id})

        # Send confirmation email
        order.send_email_confirmation()
        # Redirect to order confirmation page
        return request.redirect(f"/rifas/order/confirmation/{order.validation_code}")

    @http.route(
        ["/rifas/order/confirmation/<validation_code>"],
        type="http",
        auth="public",
        website=True,
    )
    def order_confirmation(self, validation_code, **post):
        """Display the order confirmation page"""
        order = request.env["rifas.sale_order"].sudo().search(
            [("validation_code", "=", validation_code)], limit=1
        )
        if not order:
            return request.redirect("/rifas")

        values = {
            "order": order,
            "raffle": order.rifa_id,
            "tickets": order.ticket_ids,
        }

        return request.render("rifas.rifas_order_confirmation", values)
