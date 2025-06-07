# -*- coding: utf-8 -*-
"""
Raffle Model for Rifas Module.

This module contains the main raffle model and related functionality for managing
lottery-style raffle events, including tickets, images, and associated business logic.
"""
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


def _slugify(name):
    """
    Generate a URL-friendly slug from the given name.
    
    Converts a text string into a URL-safe slug by removing special characters,
    replacing spaces with hyphens, and converting to lowercase.
    
    Args:
        name (str): The original name to be converted to a slug
        
    Returns:
        str: URL-friendly slug version of the input name
        
    Example:
        _slugify("My Raffle Name!") -> "my-raffle-name"
    """
    name = re.sub(r"[^a-zA-Z0-9\s-]", "", name)  # Remove special characters
    name = re.sub(r"\s+", "-", name)  # Replace spaces with hyphens
    name = name.strip("-")  # Remove leading/trailing hyphens
    return name.lower()  # Convert to lowercase


def _remove_html_tags(html):
    """
    Remove HTML tags from a given HTML string.
    
    Strips all HTML markup from the input string, leaving only the text content.
    
    Args:
        html (str): HTML string to clean
        
    Returns:
        str: Plain text without HTML tags
        
    Note:
        Uses regex pattern to match and remove all HTML tags (<...>)
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", html)


def _get_html_description_default():
    """
    Get the default HTML description template for new raffles.
    
    Provides a standard HTML template with placeholders for raffle information
    including event details, prizes, and promotional content.
    
    Returns:
        str: HTML template string with placeholder content
        
    Note:
        Template includes Spanish content as default for the application locale
    """
    return """
        <h1>🎉 ¡Rifa {tu rifa}! 🎉</h1>

        <p> ¡No te pierdas la oportunidad de ganar increíbles premios y apoyar una buena causa! </p>
        <ul>
        <li>🗓 Fecha de la Rifa: [Fecha de la rifa]</li>
        <li>📍 Lugar: [Ubicación del evento]</li>
        <li>⏰ Hora: [Hora del evento]</li>
        </ul>

        <p><b>Premios:<b></p>
        <ul>
        <li>🏆 Primer premio: [Descripción del primer premio]</li>
        <li>🥈 Segundo premio: [Descripción del segundo premio]</li>
        <li>🥉 Tercer premio: [Descripción del tercer premio]</li>
        </ul>
        <p>¡No te lo pierdas! Compra tus boletos ahora y participa en esta emocionante rifa. ¡Buena suerte!</p>
    """


class RifaImage(models.Model):
    """
    Model for storing raffle-related images.
    
    This model handles image storage and URL generation for raffle-related images,
    providing a centralized way to manage image assets for raffle displays.
    """
    _name = "rifas.image"
    _description = "Imagen de Rifa"

    image = fields.Binary(string="Imagen", required=True)
    image_url = fields.Char(
        string="URL de la Imagen", compute="_compute_image_url", store=True
    )
    rifa_id = fields.Many2one("rifas.raffle", string="Rifa")

    @api.depends("image")
    def _compute_image_url(self):
        """
        Compute the public URL for accessing the image.
        
        Generates a URL path that can be used to serve the image through
        the web controller endpoint.
        
        Note:
            URL format: /rifas/image/{record_id}
        """
        for record in self:
            record.image_url = f"/rifas/image/{record.id}"


class Rifa(models.Model):
    """
    Main raffle model for managing lottery-style events.
    
    This model represents a raffle event with all its associated data including
    tickets, images, sales orders, and business logic for raffle management.
    Handles the complete lifecycle from draft to finished state.
    """
    _name = "rifas.raffle"
    _description = "Rifa"

    name = fields.Char(required=True)
    description = fields.Html(
        string="Descripción", default=_get_html_description_default()
    )
    description_short = fields.Text(
        string="Descripción Corta", compute="_compute_description_short", store=True
    )
    image_feature = fields.Binary(string="Imagen Principal")
    image_feature_url = fields.Char(
        string="URL de la Imagen Principal",
        compute="_compute_image_feature_url",
        store=True,
    )
    image_ids = fields.One2many("rifas.image", "rifa_id", string="Imágenes")
    date_end = fields.Date()
    ticket_ids = fields.One2many("rifas.ticket", "rifa_id", string="Boletos")
    ticket_max = fields.Integer(string="Cantidad Máxima de Boletos")
    ticket_sold = fields.Integer(
        string="Cantidad de Boletos Vendidos",
        compute="_compute_ticket_sold",
        store=True,
    )
    ticket_available = fields.Integer(
        string="Cantidad de Boletos Disponibles",
        compute="_compute_ticket_available",
        store=True,
    )
    qty_min = fields.Integer(string="Cantidad Mínima")
    price = fields.Float(string="Precio por boleto")
    asignation_type = fields.Selection(
        [("manual", "Manual"), ("random", "Aleatorio"), ("both", "Ambos")],
        default="manual",
        required=True,
    )
    sale_order_ids = fields.One2many(
        "rifas.sale_order", "rifa_id", string="Órdenes de venta"
    )
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("publish", "Publicado"),
            ("finished", "Finalizado"),
            ("cancel", "Cancelado"),
        ],
        default="draft",
        required=True,
    )
    winning_number = fields.Integer(
        string="Número Ganador", help="Número ganador de la rifa"
    )
    winning_ticket_id = fields.Many2one(
        "rifas.ticket", string="Boleto Ganador", help="Boleto ganador de la rifa"
    )
    slug = fields.Char(string="Slug", compute="_compute_slug", store=True)
    slug_url = fields.Char(string="URL", compute="_compute_slug_url", store=True)

    @api.depends("name")
    def _compute_slug(self):
        """
        Compute the URL slug for the raffle based on its name.
        
        Generates a URL-friendly slug by combining the slugified name
        with the record ID to ensure uniqueness.
        
        Note:
            Format: {slugified_name}-{record_id}
        """
        for record in self:
            record.slug = _slugify(record.name) + "-" + str(record.id)

    @api.depends("slug")
    def _compute_slug_url(self):
        """
        Compute the public URL for the raffle based on its slug.
        
        Generates the complete URL path that can be used to access
        the raffle detail page on the website.
        
        Note:
            URL format: /rifas/{slug}
        """
        for record in self:
            record.slug_url = f"/rifas/{record.slug}"

    @api.depends("image_feature")
    def _compute_image_feature_url(self):
        """
        Compute the public URL for the raffle's main feature image.
        
        Generates a URL path that can be used to serve the main image
        through the web controller endpoint.
        
        Note:
            URL format: /rifas/image_feature/{record_id}
        """
        for record in self:
            record.image_feature_url = f"/rifas/image_feature/{record.id}"

    @api.depends("description")
    def _compute_description_short(self):
        """
        Compute a shortened version of the raffle description.
        
        Creates a truncated plain text version of the HTML description
        suitable for display in lists or previews. Removes HTML tags
        and limits to 140 characters with ellipsis if longer.
        
        Note:
            - HTML tags are stripped before truncation
            - Newlines are replaced with spaces
            - Adds "..." if description exceeds 100 characters
        """
        for record in self:
            if record.description:
                desc = _remove_html_tags(record.description)
                desc = desc.replace("\n", " ")
                record.description_short = (
                    desc[:140] + "..." if len(desc) > 100 else desc
                )
            else:
                record.description_short = ""

    @api.depends("ticket_ids")
    def _compute_ticket_sold(self):
        """
        Compute the number of tickets sold for the raffle.
        
        Calculates both the number of sold tickets and remaining available tickets.
        Ensures that sold count doesn't exceed the maximum ticket limit.
        
        Note:
            - Also updates ticket_available field
            - Prevents overselling by capping at ticket_max
        """
        for rifa in self:
            rifa.ticket_sold = len(rifa.ticket_ids.ids)
            rifa.ticket_available = rifa.ticket_max - rifa.ticket_sold
            if rifa.ticket_available < 0:
                rifa.ticket_available = 0
                rifa.ticket_sold = rifa.ticket_max

    @api.depends("ticket_max", "ticket_sold")
    def _compute_ticket_available(self):
        """
        Compute the number of tickets available for purchase.
        
        Calculates remaining tickets by subtracting sold tickets from
        the maximum allowed. Ensures the count never goes negative.
        
        Note:
            - Prevents negative values by setting minimum to 0
            - Adjusts sold count if it would exceed maximum
        """
        for rifa in self:
            rifa.ticket_available = rifa.ticket_max - rifa.ticket_sold
            if rifa.ticket_available < 0:
                rifa.ticket_available = 0
                rifa.ticket_sold = rifa.ticket_max

    def action_publish(self):
        """
        Publish the raffle after validating required fields.
        
        Performs validation checks to ensure the raffle has all necessary
        information before making it available for ticket purchases.
        Changes the state from 'draft' to 'publish'.
        
        Returns:
            bool: True if successfully published
            
        Raises:
            ValidationError: If any required field is missing:
                - description: Raffle description is required
                - image_feature: Main image is required  
                - date_end: End date is required
                - ticket_max: Maximum ticket count is required
        """
        if not self.description:
            raise ValidationError("La rifa no tiene descripción.")
        if not self.image_feature:
            raise ValidationError("La rifa no tiene imagen.")
        if not self.date_end:
            raise ValidationError("La rifa no tiene fecha de finalización.")
        if not self.ticket_max:
            raise ValidationError("La rifa no tiene cantidad máxima de boletos.")
        self.state = "publish"
        return True

    def check_number(self, number: int):
        """
        Validate if a ticket number is available for purchase.
        
        Performs comprehensive validation to ensure a ticket number
        can be assigned to a new ticket purchase.
        
        Args:
            number (int): The ticket number to validate
            
        Returns:
            bool: True if the number is valid and available
            
        Raises:
            ValidationError: For various validation failures:
                - Raffle is not published
                - Number exceeds maximum ticket count
                - Number is already assigned to another ticket
                - Number is zero or negative
        """
        if self.state != "publish":
            raise ValidationError("La rifa no está publicada.")
        if number > self.ticket_max:
            raise ValidationError("El número no es válido.")
        if number in self.ticket_ids.mapped("number"):
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
            "type": "ir.actions.act_window",
            "name": "Ordenes de Venta",
            "res_model": "rifas.sale_order",
            "view_mode": "list,form",
            "domain": [("rifa_id", "=", self.id)],
            "context": {"create": False},
        }

    def action_view_ticket(self):
        """
        This method is triggered when the user wants to view the tickets.
        It opens the ticket form view.
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Tickets",
            "res_model": "rifas.ticket",
            "view_mode": "list,form",
            "domain": [("rifa_id", "=", self.id)],
            "context": {"create": False},
        }
