# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 webkul
# Author : www.webkul.com
#
##############################################################################

import logging
from openerp.http import request
from odoo import http, SUPERUSER_ID
from odoo.exceptions import Warning
import requests
import urllib
import json
import base64
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class ClickSendNotify(http.Controller):
    @http.route(['/clicksend/notification'], type='http', auth='public', website=True, csrf=False)
    def  clicksend_notification(self, **post):
        """ Clicksend notification controller for Nudge"""
        _logger.info(
            "WEBKUL DEBUG FOR CLICKSEND: SUMMARY(POST DATA)%r", post)
        all_sms_report = request.env["sms.report"].search([('state','in',('sent','new'))])
        for sms in all_sms_report:
            if sms.clicksend_message_id and sms.clicksend_username and sms.clicksend_password and sms.clicksend_api_key:
                if post.has_key("dlrs") and post["dlrs"][0] :
                    sms_sms_obj = sms.sms_sms_id
                    if post["dlrs"][0]["status_code"] == 200:
                        _logger.info("--------Clicksend Notify----------sent---------------------------%r-------------------------", sms)
                        sms.write({'state':'sent',"status_hit_count":sms.status_hit_count + 1})
                    elif post["dlrs"][0]["status_code"] == 201:
                        _logger.info("-------------Clicksend Notify-----delivered---------------------------%r-------------------------", sms)
                        if sms.auto_delete:
                            sms.unlink()
                            if sms_sms_obj.auto_delete and not sms_sms_obj.sms_report_ids:
                                sms_sms_obj.unlink()
                        else:
                            sms.write({'state':'delivered',"status_hit_count":sms.status_hit_count + 1})
                    elif post["dlrs"][0]["status_code"] in [300,301]:
                        _logger.info("--------------Clicksend Notify---undelivered----------------------------%r-------------------------", sms)
                        sms.write({'state':'undelivered',"status_hit_count":sms.status_hit_count + 1})
                    elif post["dlrs"][0]["status_code"] == 302:
                        _logger.info("----------Clicksend Notify------Outgoing-----------------------------%r-------------------------", sms)
                        sms.write({'state':'Outgoing',"status_hit_count":sms.status_hit_count + 1})
        return

  
