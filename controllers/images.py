from odoo import http
from odoo.http import request
import base64


class RaffleImagesController(http.Controller):

    @http.route(
        "/rifas/image_feature/<int:raffle_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_raffle_image(self, raffle_id, **kwargs):
        # Buscar el registro del modelo rifas.raffles
        raffle = request.env["rifas.raffle"].sudo().browse(raffle_id)
        if not raffle or not raffle.image_feature:
            return request.not_found()

        image_data = base64.b64decode(raffle.image_feature)
        return request.make_response(
            image_data,
            headers=[
                ("Content-Type", "image/png"),
                ("Content-Length", len(image_data)),
            ],
        )

    @http.route(
        "/rifas/image/<int:image_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_image(self, image_id, **kwargs):
        # Buscar el registro del modelo rifas.image
        image_record = request.env["rifas.image"].sudo().browse(image_id)
        if not image_record or not image_record.image:
            return request.not_found()

        image_data = base64.b64decode(image_record.image)
        return request.make_response(
            image_data,
            headers=[
                ("Content-Type", "image/png"),
                ("Content-Length", len(image_data)),
            ],
        )
