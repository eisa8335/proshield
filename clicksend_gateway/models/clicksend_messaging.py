# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 webkul
# Author : www.webkul.com
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from urllib3.exceptions import HTTPError

import logging
_logger = logging.getLogger(__name__)

from urllib2 import Request, urlopen
from urllib import urlencode
import json
import base64

clicksend_send_sms_url = 'https://rest.clicksend.com/v3/sms/send'
clicksend_sms_history_url_for_REST_v3 = 'https://rest.clicksend.com/v3/sms/receipts/'
clicksend_sms_history_url_for_REST_v2 = 'https://api-mapper.clicksend.com/rest/v2/delivery.json'

CLICKSEND_FAILURE_STATUS = [
    "MISSING_CREDENTIALS",
    "ACCOUNT_NOT_ACTIVATED",
    "INVALID_RECIPIENT",
    "THROTTLED",
    "INVALID_SENDER_ID",
    "INSUFFICIENT_CREDIT",
    "INVALID_CREDENTIALS",
    "ALREADY_EXISTS",
    "MISSING_REQUIRED_FIELDS",
    "TOO_MANY_RECIPIENTS",
    "EMPTY_MESSAGE",
    "NOT_ENOUGH_PERMISSION_TO_LIST_ID",
    "INTERNAL_ERROR",
    "INVALID_VOICE",
    "SUBJECT_REQUIRED",
    "INVALID_MEDIA_FILE",
    "SOMETHING_IS_WRONG"
]
CLICKSEND_SUCCESS_STATUS = ["SUCCESS"]


def send_sms_using_clicksend(body_sms, mob_no, from_mob=None, sms_gateway=None):
    '''
    This function is designed for sending sms using clicksend SMS API.

    :param body_sms: body of sms contains text
    :param mob_no: Here mob_no must be string having one or more number seprated by (,)
    :param from_mob: sender mobile number or id used in Clicksend API
    :param sms_gateway: sms.mail.server config object for Clicksend Credentials 
    :return: response dictionary if sms successfully sent else empty dictionary
    '''
    if not sms_gateway or not body_sms or not mob_no:
        return {}
    if sms_gateway.gateway == "clicksend":
        clicksend_username = sms_gateway.clicksend_username
        clicksend_password = sms_gateway.clicksend_password
        clicksend_api_key = sms_gateway.clicksend_api_key
        try:
            if clicksend_username and clicksend_password and clicksend_api_key:
                pair_code = clicksend_username + ":" + clicksend_password
                encoded_code = base64.b64encode(pair_code)
                encoded_code_with_basic = "Basic " + encoded_code

                headers = {'Content-Type': 'application/json',
                           'Authorization': encoded_code_with_basic}

                msg_list = []
                for mobi_no in mob_no.split(','):
                    msg_dict = {"source": "python", "body": body_sms, "to": str(
                        mobi_no), "custom_string": "this is a test"}
                    msg_list.append(msg_dict)
                params = json.dumps({"messages": msg_list})
                request = Request(clicksend_send_sms_url,
                                  data=params, headers=headers)
                response_body = urlopen(request).read()
                return json.loads(response_body)
        except HTTPError as e:
            _logger.info(
                "---------------Clicksend HTTPError While Sending SMS ----%r---------", e)
            return {}
        except Exception as e:
            _logger.info(
                "---------------Clicksend Exception While Sending SMS -----%r---------", e)
            return {}
    return {}


def get_sms_history_for_clicksend(data):
    if not data:
        return {}
    if data.has_key("clicksend_message_id") and data.has_key("clicksend_username") and data.has_key("clicksend_password") and data.has_key("clicksend_api_key"):
        try:
            pair_code = data["clicksend_username"] + \
                ":" + data["clicksend_password"]
            encoded_code = base64.b64encode(pair_code)
            encoded_code_with_basic = "Basic " + encoded_code
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Authorization': encoded_code_with_basic}

            urlencode_data = {"username": data["clicksend_username"], "key": data[
                "clicksend_api_key"], "messageid": data["clicksend_message_id"]}
            values = urlencode(urlencode_data)
            request = Request(
                clicksend_sms_history_url_for_REST_v2, data=values, headers=headers)
            response_body = urlopen(request).read()
            msg_report = json.loads(response_body)
            return msg_report
        except HTTPError as e:
            _logger.info(
                "---------------Clicksend HTTPError For SMS History----%r---------", e)
            return {}
        except Exception as e:
            _logger.info(
                "---------------Clicksend Exception For SMS History-----%r---------", e)
            return {}
    return {}


class SmsSms(models.Model):
    """SMS sending using Clicksend SMS Gateway."""

    _inherit = "sms.sms"
    _name = "sms.sms"
    _description = "ClickSend SMS"

    @api.multi
    def send_sms_via_gateway(self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(SmsSms, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'clicksend':
                clicksend_username = gateway_id.clicksend_username
                clicksend_password = gateway_id.clicksend_password
                clicksend_api_key = gateway_id.clicksend_api_key
                for element in mob_no:
                    response = send_sms_using_clicksend(
                        body_sms, element, from_mob=from_mob, sms_gateway=gateway_id)
                    for mobi_no in element.split(','):
                        if response.has_key("response_code") and response["response_code"] == "SUCCESS":
                            if response.has_key("data") and response["data"].has_key("messages"):
                                for msg_report in response["data"]["messages"]:
                                    if mobi_no == msg_report["to"]:
                                        sms_report_obj = self.env["sms.report"].create(
                                            {'to': mobi_no, 'msg': body_sms, 'sms_sms_id': self.id, "auto_delete": self.auto_delete, 'sms_gateway_config_id': gateway_id.id})
                                        clicksend_message_id = msg_report[
                                            "message_id"]
                                        if msg_report["status"] in CLICKSEND_SUCCESS_STATUS:
                                            sms_report_obj.write({'state': 'sent', 'clicksend_message_id': clicksend_message_id, 'clicksend_username': clicksend_username,
                                                                  'clicksend_password': clicksend_password, 'clicksend_api_key': clicksend_api_key, })
                                        elif msg_report["status"] in CLICKSEND_FAILURE_STATUS:
                                            sms_report_obj.write({'state': 'undelivered', 'clicksend_message_id': clicksend_message_id,
                                                                  'clicksend_username': clicksend_username, 'clicksend_password': clicksend_password, 'clicksend_api_key': clicksend_api_key, })
                                        else:
                                            sms_report_obj.write({'state': 'new', 'clicksend_message_id': clicksend_message_id, 'clicksend_username': clicksend_username,
                                                                  'clicksend_password': clicksend_password, 'clicksend_api_key': clicksend_api_key, })
                        else:
                            self.write({'state': 'error'})
                else:
                    self.write({'state': 'sent'})
            else:
                gateway_id = super(SmsSms, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        else:
            _logger.info(
                "----------------------------- SMS Gateway not found -------------------------")
        return gateway_id


class SmsReport(models.Model):
    """SMS report."""

    _inherit = "sms.report"

    clicksend_message_id = fields.Char("Clicksend SMS ID")
    clicksend_username = fields.Char("Clicksend User Name")
    clicksend_password = fields.Char("Clicksend Password")
    clicksend_api_key = fields.Char("Clicksend API Key")

    @api.model
    def cron_function_for_sms(self):
        _logger.info(
            "************** Cron Function For Clicksend SMS ***********************")

        all_sms_report = self.search([('state', 'in', ('sent', 'new'))])
        for sms in all_sms_report:
            if sms.clicksend_message_id and sms.clicksend_username and sms.clicksend_password and sms.clicksend_api_key:
                msg_report = get_sms_history_for_clicksend({"clicksend_message_id": sms.clicksend_message_id, "clicksend_username": sms.clicksend_username,
                                                            "clicksend_password": sms.clicksend_password, "clicksend_api_key": sms.clicksend_api_key})
                if msg_report.has_key("dlrs") and msg_report["dlrs"][0]:
                    sms_sms_obj = sms.sms_sms_id
                    if msg_report["dlrs"][0]["status"] == "Delivered":
                        if sms.auto_delete:
                            sms.unlink()
                            if sms_sms_obj.auto_delete and not sms_sms_obj.sms_report_ids:
                                sms_sms_obj.unlink()
                        else:
                            sms.write(
                                {'state': 'delivered', "status_hit_count": sms.status_hit_count + 1})
                    elif msg_report["dlrs"][0]["status"] == "Undelivered":
                        sms.write(
                            {'state': 'undelivered', "status_hit_count": sms.status_hit_count + 1})
                    elif msg_report["dlrs"][0]["status_code"] == 200:
                        sms.write(
                            {'state': 'sent', "status_hit_count": sms.status_hit_count + 1})
                    elif msg_report["dlrs"][0]["status_code"] == 201:
                        if sms.auto_delete:
                            sms.unlink()
                            if sms_sms_obj.auto_delete and not sms_sms_obj.sms_report_ids:
                                sms_sms_obj.unlink()
                        else:
                            sms.write(
                                {'state': 'delivered', "status_hit_count": sms.status_hit_count + 1})
                    elif msg_report["dlrs"][0]["status_code"] in [300, 301]:
                        sms.write(
                            {'state': 'undelivered', "status_hit_count": sms.status_hit_count + 1})
                    elif msg_report["dlrs"][0]["status_code"] == 302:
                        sms.write(
                            {'state': 'Outgoing', "status_hit_count": sms.status_hit_count + 1})
        super(SmsReport, self).cron_function_for_sms()
        return True

    @api.multi
    def send_sms_via_gateway(self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(SmsReport, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'clicksend':
                clicksend_username = gateway_id.clicksend_username
                clicksend_password = gateway_id.clicksend_password
                clicksend_api_key = gateway_id.clicksend_api_key
                for element in mob_no:
                    count = 1
                    for mobi_no in element.split(','):
                        if count == 1:
                            self.to = mobi_no
                            rec = self
                        else:
                            rec = self.create(
                                {'to': mobi_no, 'msg': body_sms, "auto_delete": self.auto_delete, 'sms_gateway_config_id': gateway_id.id})
                        response = send_sms_using_clicksend(
                            body_sms, mobi_no, from_mob=from_mob, sms_gateway=gateway_id)
                        if response.has_key("response_code") and response["response_code"] == "SUCCESS":
                            if response.has_key("data") and response["data"].has_key("messages"):
                                for msg_report in response["data"]["messages"]:
                                    if mobi_no == msg_report["to"]:
                                        clicksend_message_id = msg_report[
                                            "message_id"]
                                        if msg_report["status"] in CLICKSEND_SUCCESS_STATUS:
                                            rec.write({'state': 'sent', 'clicksend_message_id': clicksend_message_id, 'clicksend_username': clicksend_username,
                                                       'clicksend_password': clicksend_password, 'clicksend_api_key': clicksend_api_key, })
                                        elif msg_report["status"] in CLICKSEND_FAILURE_STATUS:
                                            rec.write({'state': 'undelivered', 'clicksend_message_id': clicksend_message_id, 'clicksend_username': clicksend_username,
                                                       'clicksend_password': clicksend_password, 'clicksend_api_key': clicksend_api_key, })
                                        else:
                                            rec.write({'state': 'new', 'clicksend_message_id': clicksend_message_id, 'clicksend_username': clicksend_username,
                                                       'clicksend_password': clicksend_password, 'clicksend_api_key': clicksend_api_key, })
                        else:
                            rec.write({'state': 'undelivered'})
                        count += 1
            else:
                gateway_id = super(SmsReport, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        return gateway_id
