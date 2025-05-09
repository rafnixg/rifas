from odoo import models, fields, api

class SaleOrder(models.Model):
    _name = 'rifas.sale_order'
    _description = 'Orden de Venta'

    name = fields.Char(string='Referencia')
    create_date = fields.Datetime(
        string='Fecha de Creación',
        readonly=True,
        default=fields.Datetime.now
    )
    amount = fields.Float(string='Monto Total', compute='_compute_amount', store=True)
    email = fields.Char(string='Email', related='client_id.email', store=True)
    full_name = fields.Char(string='Nombre del cliente', related='client_id.name', store=True)
    state = fields.Selection([
        ('review', 'En revisión'),
        ('done', 'Completado'),
        ('cancel', 'Cancelado')
    ], default='review', required=True)
    client_id = fields.Many2one('rifas.client', string='Cliente', required=True)
    rifa_id = fields.Many2one('rifas.raffle', string='Rifa', required=True)
    ticket_ids = fields.One2many('rifas.ticket', 'sale_order_id', string='Tickets')
    payment_id = fields.Many2one('rifas.payment', string='Pago')
    ticket_count = fields.Integer(string='Cantidad de Boletos', compute='_compute_ticket_count', store=True)

    def _check_amount(self):
        """
        This method checks if the amount of the sale order is equal to the sum of the ticket prices.
        """
        total = 0
        for ticket in self.ticket_ids:
            total += ticket.price
        if total != self.amount:
            raise ValueError("El monto no coincide con la suma de los precios de los boletos.")

    def create(self, vals_list):
        """
        Override the create method to set the name and check the state of the rifa.
        """
        if vals_list.get('rifa_id'):
            rifa = self.env['rifas.raffle'].browse(vals_list['rifa_id'])
            if rifa.state != 'publish':
                raise ValueError("La rifa no está publicada.")

        self._check_amount()

        name = self.env['ir.sequence'].next_by_code('rifas.sale.order') or 'Nuevo'
        vals_list['name'] = name
        order = super(SaleOrder, self).create(vals_list)
        return order

    @api.onchange('state')
    def _onchange_state(self):
        """
        This method is triggered when the state of the sale order changes.
        It updates the state of the associated tickets.
        """
        if self.state == 'done':
            self.ticket_ids.write({'state': 'done'})

    @api.depends('ticket_ids')
    def _compute_amount(self):
        """
        This method computes the total amount of the sale order based on the selected tickets.
        """
        for order in self:
            total = 0
            for ticket in order.ticket_ids:
                total += ticket.price
            order.amount = total

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        """
        This method computes the number of tickets associated with the sale order.
        """
        for order in self:
            order.ticket_count = len(order.ticket_ids)

    def action_cancel(self):
        """
        This method is triggered when the sale order is canceled.
        It updates the state of the associated tickets and the sale order itself.
        """
        self.state = 'cancel'
        # self.ticket_ids.unlink()
        return True

    def set_winner(self, number):
        """
        This method sets a ticket as a winner based on the provided number.
        It raises a ValueError if no winning ticket is found.
        """
        ticket = self.ticket_ids.filtered(lambda t: t.number == number)
        if ticket:
            ticket.set_winner()
        else:
            raise ValueError("No hay boleto ganador.")

    def action_view_payment(self):
        """
        This method is triggered when the user clicks on the payment button.
        It opens the payment associated with the sale order.
        """
        return {
            'name': 'Ver Pago',
            'type': 'ir.actions.act_window',
            'res_model': 'rifas.payment',
            'view_mode': 'form',
            'res_id': self.payment_id.id,
            'target': 'current',
            'context': {
                'default_sale_order_id': self.id,
                'default_client_id': self.client_id.id,
                'default_rifa_id': self.rifa_id.id,
            }
        }