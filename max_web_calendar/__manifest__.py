# -*- coding: utf-8 -*-
{
    'name': "Web Calendar Enhancement",

    'summary': """
        To enhance official odoo web_calendar mudule.
    """,

    'description': """
        Set certain color for events based on color field value.
        Support HTML tags in display setting of the event in calendar view.
        Fix translation issue of selection and boolean type fields.
        Avoid showing false in nullable fields
        Show tooltip for each event in calendar view.

        To enable certain color feature, please add 'color_type="certain"' attribute into <calendar> tag.
        To enable tooltip feature, please add 'tooltip="tooltip_field_name"' attribute into <calendar> tag and
        '<field name="tooltip_field_name"/>' in calendar fields list.
        You need to replace tooltip_field_name with your field name.
    """,

    'author': "MAXodoo",
    'website': "http://www.maxodoo.com",
    'category': 'web',
    'version': '10.0.0.1',
    'depends': ['base', 'web_calendar'],
    'data': [
        'views/max_web_calendar_view.xml',
    ],
}
