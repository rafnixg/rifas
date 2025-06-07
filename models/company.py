# -*- coding: utf-8 -*-
"""
Company Extensions for Rifas Module.

This module extends the standard res.company model to add raffle-specific
configuration fields for email notifications and company communication settings.
"""

from odoo import models, fields, api


class RifaCompany(models.Model):
    """
    Extension of the res.company model for raffle-specific configurations.
    
    This model inherits from res.company and adds additional fields
    specific to raffle operations, particularly for email notification
    settings and communication preferences.
    """
    _inherit = "res.company"
    
    email_to = fields.Char(
        string="Email de la empresa",
        help="Email de la empresa para enviar notificaciones",
    )
    email_to_cc = fields.Char(
        string="Email CC",
        help="Email CC para enviar notificaciones",
    )
