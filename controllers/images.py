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

    @http.route(
        "/payment_method/<int:payment_method_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_payment_method_image(self, payment_method_id, **kwargs):
        """
        This method retrieves the image of a payment method based on its ID.
        :param payment_method_id: ID of the payment method.
        :return: Image data in PNG format.
        """
        payment_method = (
            request.env["rifas.payment_method"].sudo().browse(payment_method_id)
        )
        if not payment_method or not payment_method.image:
            return request.not_found()

        image_data = base64.b64decode(payment_method.image)
        return request.make_response(
            image_data,
            headers=[
                ("Content-Type", "image/png"),
                ("Content-Length", len(image_data)),
            ],
        )
