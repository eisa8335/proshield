# -*- coding: utf-8 -*-
# Part of BiztechCS. See LICENSE file for full copyright and licensing details.

{
    'name': 'Clever Multiple Invoice Template',
    'version': '10.0.1.0.2',
    'author': 'BiztechCS',
    'category': 'Accounting',
    'depends': ['report','account','sale', 'purchase'],
    'website': 'https://www.biztechconsultancy.com/',
    'description': 'Professiona Templates ,  Professional Report Templates , Customizable Invoice Templates , Multiple Professional Invoice Templates  , Customized Invoice',
    'summary': 'Get Diverse Invoice Templates In One Go!',
    'data': [ 
        'views/web_widget_color_view.xml',
        'views/template_report.xml',
        'views/creative_template.xml',
        'views/elegant_template.xml',
        'views/professional_template.xml',
        'views/exclusive_template.xml',
        'views/advanced_template.xml',
        'views/custom_template.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/invoice_view.xml',
    ],
    'qweb': [
        'static/src/xml/widget_color.xml',
    ],    
    'images': ['static/description/clever-multiple-invoice-templates-odoo-app.png'],
    'price': 29.00,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'web_preload': True,
}
