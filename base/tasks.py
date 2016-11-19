#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/19 12:56
@annotation = '' 
"""
from base import sms_util
from base.celery import app
from base.mail_util import Email
from base.sms_util import PushBullet


@app.task(routing_key="sms_remind")
def send_twilio(to, body=None):
    sms_util.send_twilio(to, body)


@app.task(exchange="sms_remind")
def send_sms_to_phone(title, body):
    PushBullet.send_sms_to_phone(title, body)


@app.task(routing_key="sms_remind")
def send_sms_to_pc(title, body):
    PushBullet.send_sms_to_pc(title, body)


@app.task(routing_key="sms_remind")
def send_email(title, body):
    PushBullet.send_email(title, body)


@app.task(routing_key="mail_remind")
def send_mail(to_addr, msg_type, subject, text, **kwargs):
    Email(to_addr, msg_type).send_email(subject, text, **kwargs)
