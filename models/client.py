from odoo import models, fields, api


class RifaClient(models.Model):
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
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    def create(self, vals_list):
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
        self.ensure_one()
        return {
            "name": "Órdenes de Venta",
            "type": "ir.actions.act_window",
            "res_model": "rifas.sale_order",
            "view_mode": "list,form",
            "domain": [("client_id", "=", self.id)],
        }