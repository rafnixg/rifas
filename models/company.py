from odoo import models, fields, api

class RifaCompany(models.Model):
    _inherit = "res.company"
    
    email_to = fields.Char(
        string="Email de la empresa",
        help="Email de la empresa para enviar notificaciones",
    )
    email_to_cc = fields.Char(
        string="Email CC",
        help="Email CC para enviar notificaciones",
    )
    