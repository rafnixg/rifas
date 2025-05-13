{
    "name": "Rifas",
    "version": "18.0.2.1.0",
    "summary": "Gestión de rifas para vertical de sorteos",
    "description": """
        Módulo para la gestión de rifas, sorteos y boletos en Odoo 18.0.
    """,
    "author": "Rafnix Guzman",
    "website": "https://rafnixg.com",
    "category": "Website",
    "depends": [
        "base",
        "mail"
    ],    "data": [
        "security/ir.model.access.csv",
        "views/payment_views.xml",
        "views/raffle_views.xml",
        "views/sale_order_views.xml",
        "views/ticket_views.xml",
        "views/client_views.xml",
        "views/website/components.xml",
        "views/website/home_template.xml",
        "views/website/validate_template.xml",
        "views/website/raffle_template.xml", 
        "views/website/checkout_template.xml",
        "views/website/confirmation_template.xml",
        "wizards/raffle_winner_views.xml",
        "data/mail_templates.xml",
        "data/ir.sequence.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "assets": {
        "web.assets_common": [
            "rifas/static/css/global.css",
        ],
        "web.assets_frontend": [
            "rifas/static/css/home.css",
            "rifas/static/css/raffle.css",
            "rifas/static/css/checkout.css",
            "rifas/static/js/raffle.js",
            "rifas/static/js/checkout.js",
        ],
    },
}
