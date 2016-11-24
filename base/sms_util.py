#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/16 23:26
@annotation = '' 
"""
import json

from base.celery import app
from etc import config
from tornado import gen
from tornado import httpclient
from tornado.escape import json_decode
from tornado.httputil import url_concat


@gen.coroutine
def post(url, headers, data=None):
    body = json.dumps(data) if isinstance(data, dict) else data
    client = httpclient.AsyncHTTPClient()
    response = yield client.fetch(url, headers=headers, body=body, method="POST")
    if response.error:
        print("Error:", response.code, response.error)
    return json_decode(response.body)


@gen.coroutine
def get(url, headers, params=None):
    url = url_concat(url, params)
    client = httpclient.AsyncHTTPClient()
    response = yield client.fetch(url, headers=headers, method="GET")
    if response.error:
        print("Error:", response.code, response.error)
    return json_decode(response.body)


class PushBullet(object):
    def __init__(self):
        self.headers = config.PUSH_BULLET.HEADERS
        self.phone_id = config.PUSH_BULLET.PHONE_ID
        self.pc_id = config.PUSH_BULLET.PC_ID
        self.push_url = config.PUSH_BULLET.PUSH_URL

    @classmethod
    def send_sms_to_phone(cls, title='', body='', device_iden=None):
        device_iden = device_iden if device_iden else cls.phone_id
        if title or body:
            data = {
                "type": "note",
                "title": title,
                "body": body,
                "device_iden": device_iden
            }
            post(cls.push_url, cls.headers, data)

    @classmethod
    def send_sms_to_pc(cls, title='', body='', device_iden=None):
        device_iden = device_iden if device_iden else cls.pc_id
        cls.send_sms_to_phone(title, body, device_iden=device_iden)

    @classmethod
    def send_email(cls, title='', body='', email=None):
        if email and (title or body):
            data = {
                "type": "note",
                "title": title,
                "body": body,
                "email": email,
            }
            post(cls.push_url, cls.headers, data)


@app.task
def send_twilio(to, body=None):
    if to.startswith("+"):
        # Download the twilio-python library from http://twilio.com/docs/libraries
        from twilio.rest import TwilioRestClient
        # Find these values at https://twilio.com/user/account
        account_sid = config.TWILIO.ACCOUNT_SID
        auth_token = config.TWILIO.AUTH_TOKEN
        client = TwilioRestClient(account_sid, auth_token)
        client.messages.create(to=to, from_=config.TWILIO.FROM, body=body)
    else:
        raise Exception("The phone number use country +86 etc")
