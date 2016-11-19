#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/16 13:44
@annotation = '' 
"""
from base import sms_util, mail_util
from base.framework import RouteCollector, BaseHandler
from tornado import gen

route = RouteCollector('remind', prefix="/remind")


@route("/main")
class MainHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # self.write("Hello world")
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("remind.main"))

    def post(self, *args, **kwargs):
        self.write("Hello world")
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("remind.main"))


@route("/simple_sms", name="simple_sms")
class SimpleSMSHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        title = self.safe_vars.title
        body = self.safe_vars.body
        sms_util.send_sms_to_phone.apply_async(args=(title, body))


@route("/simple_pc", name="simple_pc")
class SimplePCHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        title = self.safe_vars.title
        body = self.safe_vars.body
        sms_util.send_sms_to_pc.apply_async(args=(title, body))


@route("/simple_email", name="simple_email")
class SimpleEmailHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        title = self.safe_vars.title
        body = self.safe_vars.body
        email = self.safe_vars.email
        sms_util.send_email.apply_async(args=(title, body, email))


@route("/sms", name="sms")
class SMSHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        to = self.safe_vars.to
        body = self.safe_vars.body
        sms_util.send_twilio.apply_async(args=(to, body))


@route("/email")
class EmailHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        to_addr = self.safe_vars.to_addr
        msg_type = self.safe_vars.msg_type

        subject = self.safe_vars.subject
        text = self.safe_vars.text

        mail_util.send_email.apply_async(args=(to_addr, msg_type, subject, text))


@route("/attach")
class AttachHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        to_addr = self.safe_vars.to_addr
        msg_type = self.safe_vars.msg_type

        subject = self.safe_vars.subject
        text = self.safe_vars.text

        kwargs = {}
        if self.request.files:
            meta = self.request.files["file"][0]
            kwargs["file_name"] = meta["filename"]
            kwargs["content"] = meta["body"]

        # mail_util.send_email(*(to_addr, msg_type, subject, text), **kwargs)
        mail_util.send_email.apply_async(
            args=(to_addr, msg_type, subject, text), kwargs=kwargs)
