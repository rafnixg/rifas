from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PaymentMethod(models.Model):
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
        This method computes the URL for the logo image.
        """
        for record in self:
            if record.image:
                record.logo_url = f"/payment_method/{record.id}"
            else:
                record.logo_url = False



class Payment(models.Model):
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
        if vals_list.get("name", ("New")) == ("New"):
            vals_list["name"] = self.env["ir.sequence"].next_by_code(
                "rifas.payment"
            ) or ("New")
        res = super(Payment, self).create(vals_list)
        res.sale_order_id.payment_id = res.id
        return res

    def action_review(self):
        """
        This method is triggered when the payment is reviewed.
        It updates the state of the payment and the associated sale order.
        """
        self.state = "review"
        self.sale_order_id.state = "review"
        self.sale_order_id.ticket_ids.write({"state": "review"})
        return True

    def action_approve(self):
        """
        This method is triggered when the payment is approved.
        It updates the state of the payment and the associated sale order.
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
        This method sends an email to the client when the payment is approved.
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
        This method is triggered when the payment is canceled.
        It updates the state of the payment and the associated sale order.
        """
        self.state = "cancel"
        self.sale_order_id.state = "cancel"
        return True

    def action_sale_order(self):
        """
        This method is triggered when the user clicks on the sale order button.
        It opens the sale order associated with the payment.
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Órdenes de Venta",
            "res_model": "rifas.sale_order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
            "target": "current",
        }
