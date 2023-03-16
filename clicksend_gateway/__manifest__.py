# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 webkul
# Author : www.webkul.com
#
##############################################################################


{
    'name': 'ClickSend SMS Gateway',
    'version': '1.0',
    'summary':'Send sms notifications using ClickSend SMS gateway.',
    'category': 'Marketing',
    'description': """This ClickSend sms gateway is used to send the sms to the mobile numbers.""",
    "sequence": 1,
    'images':['static/description/Banner.png'],
    "author": "Webkul Software Pvt. Ltd.",
    "website": "http://www.webkul.com",
    "version": '1.0',
    'depends': ['sms_notification'],
    'data': [
        'views/clicksend_config_view.xml',
        'views/sms_report.xml',
       
        ],
    "application": True,
    'installable': True,
    'auto_install': False,
    "price": 20,
    "currency": 'EUR',
}
