{
    "name": "Rifas Management",
    "version": "18.0.1.0.0",
    "summary": "Manage raffles and tickets",
    "description": """
Rifas Management
===============
This module allows to manage raffles, tickets sales and winners.
    """,
    "author": "Rafnix Guzman",
    "website": "https://rafnixg.com",
    "category": "Website",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir.sequence.xml",
        "views/raffle_views.xml",
        "views/sale_order_views.xml",
        "views/payment_views.xml",
        "views/ticket_views.xml",
        "wizards/raffle_winner_views.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
