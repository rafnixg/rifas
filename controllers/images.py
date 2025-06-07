# -*- coding: utf-8 -*-
"""
Image controller for raffle image serving.

This module handles the serving of raffle images and related image assets
through HTTP endpoints for web display.
"""
import base64

from odoo import http
from odoo.http import request


class RaffleImagesController(http.Controller):
    """
    Controller for serving raffle and related images.
    
    This controller provides HTTP endpoints to serve images stored in the database,
    including raffle feature images and general image records.
    """

    @http.route(
        "/rifas/image_feature/<int:raffle_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_raffle_image(self, raffle_id, **kwargs):
        """
        Serve the feature image of a specific raffle.
        
        Retrieves and serves the main feature image associated with a raffle record.
        
        Args:
            raffle_id (int): The ID of the raffle to get the image for
            **kwargs: Additional request parameters (not used)
            
        Returns:
            Response: HTTP response with image data and appropriate headers
            or 404 if raffle or image not found
            
        Note:
            - Images are served as PNG format
            - CSRF protection is disabled for public access
            - Returns 404 if raffle doesn't exist or has no feature image
        """
        # Search for the raffle record
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
        """
        Serve a general image from the rifas.image model.
        
        Retrieves and serves an image from the rifas.image model records.
        
        Args:
            image_id (int): The ID of the image record to serve
            **kwargs: Additional request parameters (not used)
            
        Returns:
            Response: HTTP response with image data and appropriate headers
            or 404 if image record not found
            
        Note:
            - Images are served as PNG format
            - CSRF protection is disabled for public access
            - Returns 404 if image record doesn't exist or has no image data
        """
        # Search for the rifas.image model record
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
        Serve the image of a payment method.
        
        Retrieves and serves the image associated with a payment method record.
        
        Args:
            payment_method_id (int): The ID of the payment method to get the image for
            **kwargs: Additional request parameters (not used)
            
        Returns:
            Response: HTTP response with image data and appropriate headers
            or 404 if payment method or image not found
            
        Note:
            - Images are served as PNG format
            - CSRF protection is disabled for public access
            - Returns 404 if payment method doesn't exist or has no image
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
