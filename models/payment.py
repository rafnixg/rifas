# -*- coding: utf-8 -*-
"""
Payment Management Models for Rifas Module.

This module handles payment processing for raffle ticket purchases, including
payment method management, payment validation, approval workflows, and
customer notification systems.
"""
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PaymentMethod(models.Model):
    """
    Model representing available payment methods for raffle purchases.
    
    This model manages the different payment options available to customers,
    including their visual representation and activation status.
    """
    _name = "rifas.payment_method"
    _description = "Método de Pago"

    name = fields.Char(required=True)
    description = fields.Text()
    image = fields.Binary("Imagen")
    logo_url = fields.Char(
        string="URL de la Imagen",
        compute="_compute_logo_url",
        store=True,
    )
    is_active = fields.Boolean(default=True)

    @api.depends("image")
    def _compute_logo_url(self):
        """
        Generate URL for the payment method logo image.
        
        Creates a web-accessible URL for the payment method's logo image
        when an image is uploaded. Used for display in web interfaces.
        
        Note:
            URL is only generated if an image is present
        """
        for record in self:
            if record.image:
                record.logo_url = f"/payment_method/{record.id}"
            else:
                record.logo_url = False


class Payment(models.Model):
    """
    Model representing payments made for raffle ticket purchases.
    
    This model manages the complete payment lifecycle from submission
    to approval, including validation, state management, and customer
    communication throughout the payment process.
    """
    _name = "rifas.payment"
    _description = "Pago"
    _order = "date desc"

    name = fields.Char(
        string="Serie",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: ("New"),
    )
    full_name = fields.Char(string="Cliente", related="client_id.name", store=True)
    document_number = fields.Char(string="Número de Documento")
    phone = fields.Char(related="client_id.phone", string="Teléfono", store=True)
    email = fields.Char(related="client_id.email", string="Email", store=True)
    date = fields.Datetime(
        string="Fecha de Pago", readonly=True, default=fields.Datetime.now
    )
    payment_method_id = fields.Many2one("rifas.payment_method", string="Método de Pago")
    amount = fields.Float(string="Monto")
    reference = fields.Char(string="Referencia")
    reference_image = fields.Binary(string="Imagen del Pago")
    state = fields.Selection(
        [("review", "En revisión"), ("approve", "Aprobado"), ("cancel", "Cancelado")],
        default="review",
        required=True,
    )
    client_id = fields.Many2one("rifas.client", string="Cliente")
    partner_id = fields.Many2one(
        "res.partner", string="Socio", related="client_id.partner_id"
    )
    rifa_id = fields.Many2one("rifas.raffle", string="Rifa")
    sale_order_id = fields.Many2one("rifas.sale_order", string="Orden de Venta")

    def create(self, vals_list):
        """
        Create a new payment record with automatic sequence assignment.
        
        Overrides the default create method to assign a sequential payment number
        and automatically link the payment to its associated sale order.
        
        Args:
            vals_list (dict): Dictionary containing field values for the new payment
            
        Returns:
            Payment: Created payment instance with automatic sequence number
        """
        if vals_list.get("name", ("New")) == ("New"):
            vals_list["name"] = self.env["ir.sequence"].next_by_code(
                "rifas.payment"
            ) or ("New")
        res = super(Payment, self).create(vals_list)
        res.sale_order_id.payment_id = res.id
        return res

    def action_review(self):
        """
        Set payment status to review and update related records.
        
        Changes the payment state to 'review' and cascades this state
        to the associated sale order and its tickets for consistency.
        
        Returns:
            bool: True if the review action was successful
        """
        self.state = "review"
        self.sale_order_id.state = "review"
        self.sale_order_id.ticket_ids.write({"state": "review"})
        return True

    def action_approve(self):
        """
        Approve payment after validation and update all related records.
        
        Validates that payment amount matches sale order total, then approves
        the payment and cascades approval to sale order and tickets. Sends
        confirmation email to customer upon successful approval.
        
        Returns:
            bool: True if approval was successful
            
        Raises:
            ValidationError: If payment amount doesn't match order total
        """
        amount = self.sale_order_id.amount
        if self.amount != amount:
            raise ValidationError(
                "El monto del pago no coincide con el monto de la orden de venta."
            )

        self.state = "approve"
        self.sale_order_id.state = "done"
        self.sale_order_id.ticket_ids.write({"state": "approve"})
        # send email to client
        self._send_email_approved()
        return True

    def _send_email_approved(self):
        """
        Send payment approval notification email to customer.
        
        Uses the predefined email template to notify the customer that
        their payment has been approved. Logs any errors during email
        sending without interrupting the approval process.
        
        Note:
            Email errors are logged but do not prevent payment approval
        """
        template = self.env.ref("rifas.email_template_payment_approved")
        if template:
            try:
                template.with_context(order=self.sale_order_id).send_mail(
                    self.sale_order_id.id,
                    force_send=True,
                    email_values={
                        "email_to": self.client_id.email
                })
            except Exception as e:
                self.env["ir.logging"].create(
                {
                    "name": "Rifas Order Email",
                    "type": "server",
                    "dbname": self._cr.dbname,
                    "level": "error",
                    "message": str(e),
                    "path": __file__,
                    "func": "_send_email_approved",
                    "line": 0,
                }
            )

    def action_cancel(self):
        """
        Cancel payment and cascade cancellation to related records.
        
        Sets the payment state to 'cancel' and updates the associated
        sale order to maintain data consistency across related records.
        
        Returns:
            bool: True if cancellation was successful
        """
        self.state = "cancel"
        self.sale_order_id.state = "cancel"
        return True

    def action_sale_order(self):
        """
        Open the associated sale order in form view.
        
        Provides navigation from payment record to its related sale order
        for detailed order information and management.
        
        Returns:
            dict: Action dictionary to open sale order form view
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Órdenes de Venta",
            "res_model": "rifas.sale_order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
            "target": "current",
        }
