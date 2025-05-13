# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class RifasWinner(models.TransientModel):
    _name = "rifas.winner.wizard"
    _description = "Wizard to select a raffle winner"

    winning_number = fields.Integer(
        string="Winning Number",
        required=True,
        help="Enter the winning number for the raffle",
    )
    raffle_id = fields.Many2one(
        "rifas.raffle",
        string="Raffle",
        required=True,
        help="Select the raffle to assign the winner",
    )

    @api.constrains("winning_number")
    def _check_winning_number(self):
        for wizard in self:
            if wizard.winning_number <= 0:
                raise ValidationError(
                    _("The winning number must be greater than zero.")
                )

            # Check if the number is within the raffle's range
            if wizard.raffle_id:
                if wizard.winning_number > wizard.raffle_id.ticket_max:
                    raise ValidationError(
                        _(
                            "The winning number cannot be greater than the maximum number (%s) in the raffle.",
                            wizard.raffle_id.ticket_max,
                        )
                    )

                # Check if the number was sold
                ticket = self.env["rifas.ticket"].search(
                    [
                        ("rifa_id", "=", wizard.raffle_id.id),
                        ("number", "=", str(wizard.winning_number)),
                        ("state", "=", "approve"),
                    ],
                    limit=1,
                )

                if not ticket:
                    raise ValidationError(
                        _(
                            "The number %s has not been sold in this raffle.",
                            wizard.winning_number,
                        )
                    )

    def action_confirm_winner(self):
        """Set the winning number and mark the raffle as finished"""
        self.ensure_one()

        if self.raffle_id.state == "finished":
            raise UserError(_("This raffle is already finished with a winner."))

        if self.raffle_id.state != "publish":
            raise UserError(_("You can only select a winner for active raffles."))

        # Find the winning ticket
        winning_ticket = self.env["rifas.ticket"].search(
            [
                ("rifa_id", "=", self.raffle_id.id),
                ("number", "=", str(self.winning_number)),
                ("state", "=", "approve"),
            ],
            limit=1,
        )

        if winning_ticket:

            winning_ticket.set_winner()

            # Update raffle
            self.raffle_id.write(
                {
                    "winning_number": self.winning_number,
                    "winning_ticket_id": winning_ticket.id,
                    "state": "finished",
                }
            )

            # Create activity or notification for the winner
            self._notify_winner(winning_ticket)

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Winner Selected"),
                    "message": _(
                        "The number %s has been selected as winner for the raffle %s.",
                        self.winning_number,
                        self.raffle_id.name,
                    ),
                    "sticky": False,
                    "type": "success",
                    "next": {
                        "type": "ir.actions.act_window",
                        "res_model": "rifas.raffle",
                        "res_id": self.raffle_id.id,
                        "view_mode": "form",
                        "target": "current",
                    },
                },
            }
        else:
            raise UserError(
                _("Could not find a valid ticket with number %s", self.winning_number)
            )

    def _notify_winner(self, winning_ticket):
        """Send notification to the winner"""

        template = self.env.ref("rifas.email_template_winner_notification")
        template.sudo().send_mail(
            winning_ticket.id,
            force_send=True,
            email_values={
                "email_to": winning_ticket.client_id.email,
                "email_from": "me@rafnixg.dev",
            },
        )
