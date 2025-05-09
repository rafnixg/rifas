# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError


class RifasCheckout(http.Controller):

    @http.route(['/rifas/checkout/<int:raffle_id>'], type='http', auth="public", website=True)
    def checkout(self, raffle_id, **post):
        """Display the checkout page with selected tickets"""
        raffle = request.env['rifas.raffle'].sudo().browse(raffle_id)
        if not raffle.exists():
            return request.redirect('/')

        # Get selected tickets from session or post
        ticket_ids = post.get('ticket_ids', '')
        selected_tickets = []
        
        if ticket_ids:
            # Comma-separated list of ticket IDs
            ids = [int(x) for x in ticket_ids.split(',') if x.isdigit()]
            selected_tickets = request.env['rifas.ticket'].sudo().browse(ids)
        elif request.session.get('selected_ticket_ids'):
            # Retrieve from session
            ids = request.session.get('selected_ticket_ids', [])
            selected_tickets = request.env['rifas.ticket'].sudo().browse(ids)
        
        if not selected_tickets:
            # No tickets selected, redirect to raffle page
            return request.redirect(f'/raffle/{raffle_id}')
        # Validate that tickets are available
        unavailable_tickets = selected_tickets.filtered(lambda t: t.state != 'available')
        if unavailable_tickets:
            # Some tickets are no longer available
            return request.render('rifas.rifas_tickets_unavailable', {
                'raffle': raffle,
                'unavailable_tickets': unavailable_tickets,
            })
        
        # Calculate total amount
        total_amount = len(selected_tickets) * raffle.ticket_price
        
        # Get payment methods
        payment_methods = request.env['rifas.payment.method'].sudo().search([
            ('active', '=', True)
        ])
        
        # Try to get partner information from logged in user
        partner = request.env.user.partner_id if request.env.user.id != request.env.ref('base.public_user').id else False
        
        values = {
            'raffle': raffle,
            'selected_tickets': selected_tickets,
            'total_amount': total_amount,
            'payment_methods': payment_methods,
            'partner': partner,
            'currency': request.env.company.currency_id,
        }
        
        # Store selected ticket IDs in session
        if selected_tickets:
            request.session['selected_ticket_ids'] = selected_tickets.ids
        
        return request.render("rifas.rifas_checkout", values)

    @http.route(['/rifas/checkout/submit/<int:raffle_id>'], type='http', auth="public", website=True, methods=['POST'])
    def checkout_submit(self, raffle_id, **post):
        """Process the checkout form submission"""
        raffle = request.env['rifas.raffle'].sudo().browse(raffle_id)
        if not raffle.exists():
            return request.redirect('/rifas')
            
        # Get selected tickets from post data
        ticket_ids = post.get('ticket_ids', '')
        selected_tickets = []
        
        if ticket_ids:
            # Comma-separated list of ticket IDs
            ids = [int(x) for x in ticket_ids.split(',') if x.isdigit()]
            selected_tickets = request.env['rifas.ticket'].sudo().browse(ids)
        elif request.session.get('selected_ticket_ids'):
            # Retrieve from session
            ids = request.session.get('selected_ticket_ids', [])
            selected_tickets = request.env['rifas.ticket'].sudo().browse(ids)
            
        if not selected_tickets:
            return request.redirect(f'/raffle/{raffle_id}')
            
        # Validate that tickets are available
        unavailable_tickets = selected_tickets.filtered(lambda t: t.state != 'available')
        if unavailable_tickets:
            return request.render('rifas.rifas_tickets_unavailable', {
                'raffle': raffle,
                'unavailable_tickets': unavailable_tickets,
            })
            
        # Create or update partner
        partner_values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'street': post.get('address'),
            'vat': post.get('document'),
        }
        
        # Find existing partner by email
        partner = request.env['res.partner'].sudo().search([
            ('email', '=', post.get('email'))
        ], limit=1)
        
        if partner:
            # Update existing partner
            partner.sudo().write(partner_values)
        else:
            # Create new partner
            partner = request.env['res.partner'].sudo().create(partner_values)
            
        # Calculate total amount
        total_amount = len(selected_tickets) * raffle.ticket_price
            
        # Create the sale order
        order_values = {
            'partner_id': partner.id,
            'raffle_id': raffle.id,
            'amount_total': total_amount,
            'payment_method_id': int(post.get('payment_method')) if post.get('payment_method') else False,
            'payment_reference': post.get('payment_reference', ''),
            'notes': post.get('payment_notes', ''),
        }
        
        order = request.env['rifas.order'].sudo().create(order_values)
        
        # Link tickets to the order and mark them as reserved
        selected_tickets.sudo().write({
            'state': 'reserved',
            'partner_id': partner.id,
            'order_id': order.id,
        })
        
        # Clear session data
        if 'selected_ticket_ids' in request.session:
            del request.session['selected_ticket_ids']
            
        # Send confirmation email
        try:
            template = request.env.ref('rifas.email_template_order_confirmation')
            if template:
                template.sudo().with_context(order=order).send_mail(
                    order.id, force_send=True, email_values={'email_to': partner.email}
                )
        except Exception as e:
            # Log the error but continue the process
            request.env['ir.logging'].sudo().create({
                'name': 'Rifas Order Email',
                'type': 'server',
                'dbname': request.env.cr.dbname,
                'level': 'error',
                'message': str(e),
            })
            
        return request.redirect(f'/rifas/order/confirmation/{order.id}')
        
    @http.route(['/rifas/order/confirmation/<int:order_id>'], type='http', auth="public", website=True)
    def order_confirmation(self, order_id, **post):
        """Display the order confirmation page"""
        order = request.env['rifas.order'].sudo().browse(order_id)
        if not order.exists():
            return request.redirect('/rifas')
            
        values = {
            'order': order,
            'raffle': order.raffle_id,
            'tickets': order.ticket_ids,
        }
        
        return request.render("rifas.rifas_order_confirmation", values)