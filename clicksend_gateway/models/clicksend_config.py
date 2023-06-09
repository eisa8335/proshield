# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 webkul
# Author : www.webkul.com
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import except_orm
from openerp.exceptions import except_orm, Warning, RedirectWarning
from clicksend_messaging import send_sms_using_clicksend
import logging
_logger = logging.getLogger(__name__)


class SmsMailServer(models.Model):
    """Configure the clicksend sms gateway."""

    _inherit = "sms.mail.server"
    _name = "sms.mail.server"
    _description = "Clicksend"

    clicksend_username = fields.Char(string="Clicksend Username")
    clicksend_password = fields.Char(string="Clicksend Password")
    clicksend_api_key = fields.Char(string="Clicksend Api key")

    @api.one
    def test_conn_clicksend(self):
        sms_body = "Clicksend Test Connection Successful........"
        mobile_number = self.user_mobile_no
        response = send_sms_using_clicksend(
            sms_body, mobile_number, sms_gateway=self)

        if response.has_key("response_code") and response["response_code"] == "SUCCESS":
            if self.sms_debug:
                _logger.info(
                    "===========Test Connection status has been sent on %r mobile number", mobile_number)
            raise Warning(
                "Test Connection status has been sent on %s mobile number" % mobile_number)

        if response.has_key("response_code") and response["response_code"] in ("BAD_REQUEST", "UNAUTHORIZED"):
            if self.sms_debug:
                _logger.error(
                    "==========One of the information given by you is wrong. It may be [Mobile Number] [Username] or [Password] or [Api key]")
            raise Warning(
                "One of the information given by you is wrong. It may be [Mobile Number] [Username] or [Password] or [Api key]")

    @api.model
    def get_reference_type(self):
        selection = super(SmsMailServer, self).get_reference_type()
        selection.append(('clicksend', 'ClickSend'))
        return selection
