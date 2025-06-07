# -*- coding: utf-8 -*-
"""
Sale Order Model for Rifas Module.

This module handles the sale order management for raffle ticket purchases,
including order validation, payment tracking, and customer communication.
"""
import hashlib

from odoo import models, fields, api

STATE_SALE_ORDER = [
    ("review", "En revisión"),
    ("done", "Completado"),
    ("cancel", "Cancelado"),
]


class SaleOrder(models.Model):
    """
    Model representing sale orders for raffle ticket purchases.
    
    This model manages the complete sales process from order creation
    to completion, including ticket assignment, payment tracking,
    and customer validation through email confirmation.
    """
    _name = "rifas.sale_order"
    _description = "Orden de Venta"
    _order = "create_date desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Referencia")
    create_date = fields.Datetime(
        string="Fecha de Creación", readonly=True, default=fields.Datetime.now
    )
    amount = fields.Float(string="Monto Total", compute="_compute_amount", store=True)
    email = fields.Char(string="Email", related="client_id.email", store=True)
    full_name = fields.Char(
        string="Nombre del cliente", related="client_id.name", store=True
    )
    validation_code = fields.Char(
        string="Código de Validación", help="Código de validación para el cliente"
    )
    state = fields.Selection(
        STATE_SALE_ORDER,
        default="review",
        required=True,
    )
    client_id = fields.Many2one("rifas.client", string="Cliente", required=True)
    partner_id = fields.Many2one(
        "res.partner", string="Socio", related="client_id.partner_id"
    )
    rifa_id = fields.Many2one("rifas.raffle", string="Rifa", required=True)
    ticket_ids = fields.One2many("rifas.ticket", "sale_order_id", string="Tickets")
    payment_id = fields.Many2one("rifas.payment", string="Pago")
    ticket_count = fields.Integer(
        string="Cantidad de Boletos", compute="_compute_ticket_count", store=True
    )

    def _generate_validation_code(self):
        """
        Generate a unique validation code for the sale order.
        
        Creates an 8-character validation code using MD5 hash of the order ID
        and current timestamp. Ensures uniqueness by regenerating if code already exists.
        
        Returns:
            str: 8-character unique validation code
            
        Note:
            Recursively regenerates if duplicate code is found
        """
        code = hashlib.md5(
            (str(self.id) + fields.Datetime.now().strftime("%Y%m%d%H%M%S")).encode()
        ).hexdigest()
        validation_code = code[:8]
        validation_obj = self.env["rifas.sale_order"].search([("validation_code", "=", validation_code)])
        if validation_obj:
            # If the code already exists, generate a new one
            return self._generate_validation_code()
        return validation_code

    def _check_amount(self):
        """
        Validate that the order amount matches the sum of ticket prices.
        
        Ensures data integrity by verifying that the total order amount
        equals the sum of all associated ticket prices.
        
        Raises:
            ValueError: If the amount doesn't match the sum of ticket prices
            
        Note:
            Should be called before finalizing an order
        """
        total = 0
        for ticket in self.ticket_ids:
            total += ticket.price
        if total != self.amount:
            raise ValueError(
                "El monto no coincide con la suma de los precios de los boletos."
            )

    def create(self, vals_list):
        """
        Create a new sale order with validation and automatic field assignment.
        
        Overrides the default create method to validate raffle state, set order name
        using sequence, generate validation code, and perform amount validation.
        
        Args:
            vals_list (dict): Dictionary containing field values for the new record
            
        Returns:
            SaleOrder: Created sale order instance
            
        Raises:
            ValueError: If raffle is not published or amount validation fails
        """
        if vals_list.get("rifa_id"):
            rifa = self.env["rifas.raffle"].browse(vals_list["rifa_id"])
            if rifa.state != "publish":
                raise ValueError("La rifa no está publicada.")

        # Check amount after creating the order
        self._check_amount()
        # Set the name of the order using the sequence
        name = self.env["ir.sequence"].next_by_code("rifas.sale.order") or "Nuevo"
        vals_list["name"] = name
        # set validation code
        vals_list["validation_code"] = self._generate_validation_code()
        order = super(SaleOrder, self).create(vals_list)
        return order

    @api.onchange("state")
    def _onchange_state(self):
        """
        Handle state changes and update associated tickets accordingly.
        
        Triggered when the sale order state changes. When the order is marked
        as 'done', all associated tickets are also marked as 'done'.
        
        Note:
            This ensures data consistency between orders and tickets
        """
        if self.state == "done":
            self.ticket_ids.write({"state": "done"})

    @api.depends("ticket_ids")
    def _compute_amount(self):
        """
        Calculate the total amount based on associated ticket prices.
        
        Computes the total order amount by summing up the prices of all
        tickets associated with this sale order.
        
        Note:
            This is a computed field that automatically updates when tickets change
        """
        for order in self:
            total = 0
            for ticket in order.ticket_ids:
                total += ticket.price
            order.amount = total

    @api.depends("ticket_ids")
    def _compute_ticket_count(self):
        """
        Calculate the number of tickets associated with the sale order.
        
        Computes the total count of tickets linked to this sale order
        for display and reporting purposes.
        
        Note:
            This is a computed field that automatically updates when tickets change
        """
        for order in self:
            order.ticket_count = len(order.ticket_ids)

    def action_cancel(self):
        """
        Cancel the sale order and update associated tickets.
        
        Sets the sale order state to 'cancel'. Associated tickets remain
        in the system but are no longer active for this order.
        
        Returns:
            bool: True if cancellation was successful
            
        Note:
            Tickets are not deleted, only the order state changes
        """
        self.state = "cancel"
        # self.ticket_ids.unlink()
        return True
    def set_winner(self, number):
        """
        Set a specific ticket as winner based on the provided number.
        
        Searches for a ticket with the specified number within this order's
        tickets and marks it as the winner.
        
        Args:
            number (int): The ticket number to mark as winner
            
        Raises:
            ValueError: If no ticket with the provided number is found
        """
        ticket = self.ticket_ids.filtered(lambda t: t.number == number)
        if ticket:
            ticket.set_winner()
        else:
            raise ValueError("No hay boleto ganador.")
    def action_view_payment(self):
        """
        Open the payment view associated with this sale order.
        
        Returns an action to display the payment form related to this order,
        pre-populated with order context information.
        
        Returns:
            dict: Action dictionary for opening payment form
        """
        return {
            "name": "Ver Pago",
            "type": "ir.actions.act_window",
            "res_model": "rifas.payment",
            "view_mode": "form",
            "res_id": self.payment_id.id,
            "target": "current",
            "context": {
                "default_sale_order_id": self.id,
                "default_client_id": self.client_id.id,
                "default_rifa_id": self.rifa_id.id,
            },
        }
    def send_email_confirmation(self):
        """
        Send order confirmation email to the client.
        
        Uses the predefined email template to send a confirmation email
        to the client. Logs any errors that occur during the sending process
        without interrupting the main workflow.
        
        Note:
            Errors are logged but do not stop the order process
        """
        try:
            template = self.env.ref("rifas.email_template_order_confirmation")
            if template:
                
                template.with_context(order=self).with_company(self.env.company).send_mail(
                    self.id, force_send=True, email_values={
                        "email_to": self.client_id.email,
                        }
                )
        except Exception as e:
            # Log the error but continue the process
            self.env["ir.logging"].create(
                {
                    "name": "Rifas Order Email",
                    "type": "server",
                    "dbname": self._cr.dbname,
                    "level": "error",
                    "message": str(e),
                    "path": __file__,
                    "func": "send_email_confirmation",
                    "line": 0,
                }
            )
