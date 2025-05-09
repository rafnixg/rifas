from odoo import http
from odoo.http import request

class RaffleController(http.Controller):

    @http.route('/rifas/<slug>', type='http', auth='public', website=True)
    def view_raffle(self, slug, **kwargs):
        # Buscar la rifa por su ID
        rifa = request.env['rifas.raffle'].sudo().search([('slug', '=', slug)], limit=1)
        # Verificar si la rifa existe
        if not rifa.exists():
            return request.not_found()

        tickets_sold = rifa.ticket_ids.mapped('number') # str to int
        tickets_sold = [int(ticket) for ticket in tickets_sold]
        tickets_totales = list(range(1, rifa.ticket_max))
        tickets_disp = list(set(tickets_totales) - set(tickets_sold))
        tickets_disponibles_dict = [
            {
                'number': number,
                'price': rifa.price,
            }
            for number in tickets_disp
        ]
        # Renderizar la vista con la plantilla y los datos de la rifa
        return request.render('rifas.raffle_template', {
            'rifa': rifa,
            'payments_method': request.env['rifas.payment_method'].sudo().search([]),
            'tickets_disponibles': tickets_disponibles_dict,
        })