#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/16 23:26
@annotation = '' 
"""
import json

import requests
from base.celery import app
from etc import config


def post(url, headers, data=None):
    body = json.dumps(data) if isinstance(data, dict) else data
    resp = requests.post(url, headers=headers, data=body)
    resp.encoding = 'utf-8'
    resp_json = resp.json()
    return resp_json


def get(url, headers, params=None):
    resp = requests.get(url, headers=headers, params=params)
    resp.encoding = 'utf-8'
    resp_json = resp.json()
    return resp_json


class PushBullet(object):
    headers = config.PUSH_BULLET.HEADERS
    phone_id = config.PUSH_BULLET.PHONE_ID
    pc_id = config.PUSH_BULLET.PC_ID
    push_url = config.PUSH_BULLET.PUSH_URL

    @classmethod
    def send_sms_to_phone(cls, title='', body='', device_iden=phone_id):
        if title or body:
            data = {
                "type": "note",
                "title": title,
                "body": body,
                "device_iden": device_iden
            }
            post(cls.push_url, cls.headers, data)

    @classmethod
    def send_sms_to_pc(cls, title='', body='', device_iden=pc_id):
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


@app.task
def send_sms_to_phone(title, body):
    PushBullet.send_sms_to_phone(title, body)


@app.task
def send_sms_to_pc(title, body):
    PushBullet.send_sms_to_pc(title, body)


@app.task
def send_email(title, body, email):
    PushBullet.send_email(title, body, email)
