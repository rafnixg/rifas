from odoo import models, fields, api

class RifaClient(models.Model):
    _name = 'rifas.client'
    _description = 'Cliente de Rifa'

    name = fields.Char(string='Nombre', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Teléfono')
    state = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], default='active', string='Estado')

    # ticket_ids = fields.One2many('rifas.ticket', 'client_id', string='Tickets')
    # ruffle_ids = fields.One2many('rifas.raffle', 'client_id', string='Rifas')
    # sale_order_ids = fields.One2many('rifas.sale_order', 'client_id', string='Órdenes de Venta')
    # payment_ids = fields.One2many('rifas.payment', 'client_id', string='Pagos')

    def create(self, vals_list):
        val_email = vals_list.get('email')
        existing_client = self.search([('email', '=', val_email)], limit=1)
        if existing_client:
            existing_client.write(vals_list)
            return existing_client
        return super(RifaClient, self).create(vals_list)
