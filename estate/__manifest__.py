{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'mail', 'website'],
    'author': "Patrick Isaiah",
    'category': 'Real Estate Management',
    'description': """
        A real estate demo app
    """,
    'summary': 'A real estate application',
    'application': True,
    'license': 'LGPL-3',


    'data': [
        'views/estate_menus.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',

        'security/estate_security.xml',
        'security/ir.model.access.csv',

        'views/templates.xml',

        'data/ir_sequence_data.xml',

        'report/property_offer_template.xml',
        'report/property_offer_report.xml',

        'views/website_form.xml',
    ]
}
