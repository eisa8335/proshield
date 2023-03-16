# -*- encoding: utf-8 -*-
###########################################################################
#    Copyright (C) 2016 - Turkesh Patel. <http://turkeshpatel.odoo.com>
#
#    @author Turkesh Patel <turkesh4friends@gmail.com>
###########################################################################

{
    'name': 'Document Management System',
    'version': '1.0.1',
    'category': 'Document Management',
    'author': 'Turkesh Patel',
    'summary': """Document Management System to manage your company documents inside odoo properly.
    """,
    'description': """Document Management System to manage your company documents inside odoo properly.
    """,
    'website': 'https://turkeshpatel.odoo.com',
    'depends': ['base', 'document', 'mail', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/document_management_view.xml',
    ],
    'images': [
        'static/description/document_management_cover.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 36,
    'currency': 'EUR',
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
