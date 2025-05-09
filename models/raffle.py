from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RifaImage(models.Model):
    _name = 'rifas.image'
    _description = 'Imagen de Rifa'

    image = fields.Binary(string='Imagen')
    image_url = fields.Char(string='URL de la Imagen', compute='_compute_image_url', store=True)
    rifa_id = fields.Many2one('rifas.raffle', string='Rifa')

    @api.depends('image')
    def _compute_image_url(self):
        for record in self:
            if record.image:
                record.image_url = f"data:image/png;base64,{record.image.decode('utf-8')}"
            else:
                record.image_url = False


class Rifa(models.Model):
    _name = 'rifas.raffle'
    _description = 'Rifa'

    name = fields.Char(required=True)
    description = fields.Text()
    image_feature = fields.Binary(string='Imagen Principal')
    image_ids = fields.One2many('rifas.image', 'rifa_id', string='Imágenes')
    date_end = fields.Date()
    ticket_ids = fields.One2many('rifas.ticket', 'rifa_id', string='Boletos')
    ticket_max = fields.Integer(string='Cantidad Máxima de Boletos')
    ticket_sold = fields.Integer(string='Cantidad de Boletos Vendidos', compute='_compute_ticket_sold', store=True)
    ticket_available = fields.Integer(string='Cantidad de Boletos Disponibles', compute='_compute_ticket_available', store=True)
    qty_min = fields.Integer(string='Cantidad Mínima')
    price = fields.Float(string='Precio por boleto')
    asignation_type = fields.Selection([
        ('manual', 'Manual'),
        ('random', 'Aleatorio'),
        ('both', 'Ambos')
    ], default='manual', required=True)
    sale_order_ids = fields.One2many('rifas.sale_order', 'rifa_id', string='Órdenes de venta')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('publish', 'Publicado'),
        ('finished', 'Finalizado'),
        ('cancel', 'Cancelado')
    ], default='draft', required=True)
    winning_number = fields.Integer(string='Número Ganador', help='Número ganador de la rifa')
    winning_ticket_id = fields.Many2one('rifas.ticket', string='Boleto Ganador', help='Boleto ganador de la rifa')


    @api.depends('ticket_ids')
    def _compute_ticket_sold(self):
        """
        This method computes the number of tickets sold for the raffle.
        """
        for rifa in self:
            rifa.ticket_sold = len(rifa.ticket_ids.ids)
            rifa.ticket_available = rifa.ticket_max - rifa.ticket_sold
            if rifa.ticket_available < 0:
                rifa.ticket_available = 0
                rifa.ticket_sold = rifa.ticket_max

    @api.depends('ticket_max', 'ticket_sold')
    def _compute_ticket_available(self):
        """
        This method computes the number of tickets available for the raffle.
        """
        for rifa in self:
            rifa.ticket_available = rifa.ticket_max - rifa.ticket_sold
            if rifa.ticket_available < 0:
                rifa.ticket_available = 0
                rifa.ticket_sold = rifa.ticket_max



    def action_publish(self):
        """
        This method is triggered when the rifa is published.
        It checks if the rifa has enough tickets and updates the state to 'publish'.
        """
        if not self.description:
            raise ValidationError("La rifa no tiene descripción.")
        if not self.image_feature:
            raise ValidationError("La rifa no tiene imagen.")
        if not self.date_end:
            raise ValidationError("La rifa no tiene fecha de finalización.")
        if not self.ticket_max:
            raise ValidationError("La rifa no tiene cantidad máxima de boletos.")
        if not self.ticket_sold:
            raise ValidationError("La rifa no tiene cantidad de boletos vendidos.")
        self.state = 'publish'
        return True

    def action_winner(self):
        """
        This method is triggered when the rifa is finished.
        It checks if the rifa has enough tickets and updates the state to 'finish'.
        """
        self.state = 'finish'
        return True

    def check_number(self, number:int):
        """
        This method checks if the provided number is valid for the rifa.
        Returns True if valid, False otherwise.
        """
        if self.state != 'publish':
            raise ValidationError("La rifa no está publicada.")
        if number > self.ticket_max:
            raise ValidationError("El número no es válido.")
        if number in self.ticket_ids.mapped('number'):
            raise ValidationError("El número ya está asignado a otro boleto.")
        if number <= 0:
            raise ValidationError("El número no es válido.")
        return True
    
    def action_view_sale_order(self):
        """
        This method is triggered when the user wants to view the sale order.
        It opens the sale order form view.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ordenes de Venta',
            'res_model': 'rifas.sale_order',
            'view_mode': 'list,form',
            'domain': [('rifa_id', '=', self.id)],
            'context': {'create': False}
        }

    def action_view_ticket(self):
        """
        This method is triggered when the user wants to view the tickets.
        It opens the ticket form view.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'res_model': 'rifas.ticket',
            'view_mode': 'list,form',
            'domain': [('rifa_id', '=', self.id)],
            'context': {'create': False}
        }
