# -*- coding: utf-8 -*-
{
    'name': "Web Custom Branding",

    'summary': """
        To replace odoo branding elements from backend with custom brand.
    """,

    'description': """
        To replace odoo branding elements from backend with custom brand.
    """,

    'author': "MAXodoo",
    'website': "http://www.maxodoo.com",
    'category': 'web',
    'version': '10.0.0.1',
    'depends': ['base', 'website'],
    'data': [
        'data/max_web_custom_branding_data.xml',
        'views/max_web_custom_branding_view.xml',
    ],
    'qweb': [
        'static/src/xml/max_web_custom_branding_template.xml',
    ],
}
