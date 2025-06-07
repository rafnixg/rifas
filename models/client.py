# -*- coding: utf-8 -*-
"""
Client Management Model for Rifas Module.

This module handles customer/client management for the raffle system,
including client registration, partner integration, and sales tracking.
"""
from odoo import models, fields, api


class RifaClient(models.Model):
    """
    Model representing clients/customers in the raffle system.
    
    This model manages customer information, integrates with Odoo's partner
    system, and tracks customer activity including sales orders and purchases.
    It implements a unique email constraint to prevent duplicate customers.
    """
    _name = "rifas.client"
    _description = "Cliente de Rifa"

    name = fields.Char(string="Nombre", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Teléfono")
    state = fields.Selection(
        [("active", "Activo"), ("inactive", "Inactivo")],
        default="active",
        string="Estado",
    )
    partner_id = fields.Many2one("res.partner", string="Socio")
    sale_order_count = fields.Integer(
        string="Órdenes de Venta",
        compute="_compute_sale_order_count",
        store=True,
    )

    # ticket_ids = fields.One2many('rifas.ticket', 'client_id', string='Tickets')
    # ruffle_ids = fields.One2many('rifas.raffle', 'client_id', string='Rifas')
    sale_order_ids = fields.One2many('rifas.sale_order', 'client_id', string='Órdenes de Venta')
    # payment_ids = fields.One2many('rifas.payment', 'client_id', string='Pagos')

    @api.depends("sale_order_ids")
    def _compute_sale_order_count(self):
        """
        Calculate the total number of sale orders for this client.
        
        Computes the count of sale orders associated with this client
        for display in views and reports.
        
        Note:
            This is a computed field that updates automatically when orders change
        """
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    def create(self, vals_list):
        """
        Create a new client or update existing one if email already exists.
        
        Implements a unique email constraint by checking for existing clients
        with the same email. If found, updates the existing record instead
        of creating a duplicate. Also automatically creates a corresponding
        res.partner record for Odoo integration.
        
        Args:
            vals_list (dict): Dictionary containing field values for the new client
            
        Returns:
            RifaClient: Created or updated client instance
            
        Note:
            Automatically creates a res.partner record for integration with other Odoo modules
        """
        val_email = vals_list.get("email")
        existing_client = self.search([("email", "=", val_email)], limit=1)
        if existing_client:
            existing_client.write(vals_list)
            return existing_client
        # create partner
        partner_vals = {
            "name": vals_list.get("name"),
            "email": vals_list.get("email"),
            "phone": vals_list.get("phone"),
        }
        partner = self.env["res.partner"].create(partner_vals)
        vals_list["partner_id"] = partner.id
        return super(RifaClient, self).create(vals_list)

    def action_view_sales(self):
        """
        Open a view showing all sale orders for this client.
        
        Provides navigation from client record to their associated sale orders
        for detailed purchase history and order management.
        
        Returns:
            dict: Action dictionary to open filtered sale orders list view
        """
        self.ensure_one()
        return {
            "name": "Órdenes de Venta",
            "type": "ir.actions.act_window",
            "res_model": "rifas.sale_order",
            "view_mode": "list,form",
            "domain": [("client_id", "=", self.id)],
        }