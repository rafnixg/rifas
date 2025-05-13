import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


def _slugify(name):
    """
    This method generates a slug from the given name.
    """
    name = re.sub(r"[^a-zA-Z0-9\s-]", "", name)  # Remove special characters
    name = re.sub(r"\s+", "-", name)  # Replace spaces with hyphens
    name = name.strip("-")  # Remove leading/trailing hyphens
    return name.lower()  # Convert to lowercase


def _remove_html_tags(html):
    """
    This method removes HTML tags from the given string.
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", html)


def _get_html_description_default():
    """
    This method returns the default HTML description for the raffle.
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
    _name = "rifas.image"
    _description = "Imagen de Rifa"

    image = fields.Binary(string="Imagen", required=True)
    image_url = fields.Char(
        string="URL de la Imagen", compute="_compute_image_url", store=True
    )
    rifa_id = fields.Many2one("rifas.raffle", string="Rifa")

    @api.depends("image")
    def _compute_image_url(self):
        for record in self:
            record.image_url = f"/rifas/image/{record.id}"


class Rifa(models.Model):
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
        This method computes the slug for the raffle based on its name.
        """
        for record in self:
            record.slug = _slugify(record.name)

    @api.depends("slug")
    def _compute_slug_url(self):
        """
        This method computes the URL for the raffle based on its slug.
        """
        for record in self:
            record.slug_url = f"/rifas/{record.slug}"

    @api.depends("image_feature")
    def _compute_image_feature_url(self):
        """
        This method computes the URL for the main image of the raffle.
        """
        for record in self:
            record.image_feature_url = f"/rifas/image_feature/{record.id}"

    @api.depends("description")
    def _compute_description_short(self):
        """
        This method computes a short description for the raffle.
        It limits the description to 100 characters.
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
        This method computes the number of tickets sold for the raffle.
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
        self.state = "publish"
        return True


    def check_number(self, number: int):
        """
        This method checks if the provided number is valid for the rifa.
        Returns True if valid, False otherwise.
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
