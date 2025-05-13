from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Ticket(models.Model):
    _name = "rifas.ticket"
    _description = "Boleto de Rifa"

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
        This method computes the name of the ticket based on the raffle and number.
        """
        for record in self:
            if record.rifa_id and record.number:
                record.name = f"{record.rifa_id.name} | [{record.number}]"
            else:
                record.name = "Nuevo"

    def set_winner(self):
        """
        This method sets the ticket as a winner if the state is 'approve'.
        """
        if self.state == "approve":
            self.is_winner = True

    def create(self, vals_list):
        """
        Override the create method to set the name and check the state of the rifa.
        """
        for val in vals_list:
            rifa = self.env["rifas.raffle"].browse(val.get("rifa_id"))
            number = int(val.get("number"))
            rifa.check_number(number)
        return super(Ticket, self).create(vals_list)
