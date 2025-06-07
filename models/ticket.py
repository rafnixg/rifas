# -*- coding: utf-8 -*-
"""
Ticket Model for Rifas Module.

This module handles raffle ticket management including ticket creation,
assignment, state tracking, and winner determination functionality.
"""
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Ticket(models.Model):
    """
    Model representing individual raffle tickets.
    
    This model manages raffle tickets with their associated numbers, clients,
    payments, and state tracking throughout the raffle lifecycle.
    """
    _name = "rifas.ticket"
    _description = "Boleto de Rifa"
    _order = "create_date desc"

    rifa_id = fields.Many2one("rifas.raffle", string="Rifa", required=True)
    number = fields.Char(required=True)
    is_winner = fields.Boolean(default=False)
    sale_order_id = fields.Many2one("rifas.sale_order", string="Orden de venta")
    state = fields.Selection(
        [("review", "En revisión"), ("approve", "Aprobado")],
        default="review",
        required=True,
    )
    client_id = fields.Many2one("rifas.client", string="Cliente", required=True)
    partner_id = fields.Many2one(
        "res.partner", string="Socio", related="client_id.partner_id"
    )
    payment_id = fields.Many2one("rifas.payment", string="Pago")
    price = fields.Float(string="Precio", related="rifa_id.price", store=True)
    date = fields.Datetime(
        string="Fecha de creación", readonly=True, default=fields.Datetime.now
    )
    name = fields.Char(string="Referencia", compute="_compute_name", store=True)

    @api.depends("rifa_id", "number")
    def _compute_name(self):
        """
        Compute the display name for the ticket.
        
        Creates a descriptive name combining the raffle name and ticket number
        for easy identification in lists and forms.
        
        Format: "{raffle_name} | [{ticket_number}]"
        
        Note:
            Returns "Nuevo" (New) if raffle or number is not set
        """
        for record in self:
            if record.rifa_id and record.number:
                record.name = f"{record.rifa_id.name} | [{record.number}]"
            else:
                record.name = "Nuevo"

    def set_winner(self):
        """
        Mark this ticket as the winning ticket.
        
        Sets the is_winner flag to True if the ticket is in approved state.
        Only approved tickets can be designated as winners.
        
        Note:
            Ticket must be in 'approve' state to be set as winner
        """
        if self.state == "approve":
            self.is_winner = True

    def create(self, vals_list):
        """
        Override create method to validate ticket numbers before creation.
        
        Performs validation on each ticket before creation by checking
        if the ticket number is available for the associated raffle.
        
        Args:
            vals_list (list): List of dictionaries containing field values
            
        Returns:
            recordset: Created ticket records
            
        Note:
            Calls raffle.check_number() to validate ticket availability
        """
        for val in vals_list:
            rifa = self.env["rifas.raffle"].browse(val.get("rifa_id"))
            number = int(val.get("number"))
            rifa.check_number(number)
        return super(Ticket, self).create(vals_list)
