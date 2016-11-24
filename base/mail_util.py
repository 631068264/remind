#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/17 00:26
@annotation = '' 
"""
import mimetypes
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.utils import parseaddr

from base.celery import app
from etc import config


class BaseEmail(object):
    def __init__(self, to_addr, msg_type):
        self.from_addr = config.EMAIL.FROM_ADDR
        self.password = config.EMAIL.PASSWORD
        self.smtp_server = config.EMAIL.SMTP_SERVER
        self.encoding = config.EMAIL.ENCONDING

        self.to_addr = to_addr
        if msg_type in ('plain', 'html'):
            self.msg_type = msg_type
        else:
            raise Exception("msg_type should is plain or html")

        self.from_name = ""
        self.to_name = ""

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((self._encode(name), addr))

    def _send_email(self, msg):
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        server.quit()

    def _encode(self, msg):
        return Header(msg, self.encoding).encode()

    def _get_msg(self, subject):
        msg = MIMEMultipart()
        msg['From'] = self._format_addr('%s <%s>' % (self.from_name, self.from_addr))
        msg['To'] = self._format_addr('%s <%s>' % (self.to_name, self.to_addr))
        msg['Subject'] = self._encode(subject)
        return msg

    def _get_content_type(self, name):
        content_type, encoding = mimetypes.guess_type(name, strict=False)
        content_type = content_type or "application/octet-stream"
        maintype, subtype = content_type.split("/")
        return maintype, subtype, encoding

    def _send_file(self, file_name, content=None):
        maintype, subtype, _ = self._get_content_type(file_name)
        # maintype, subtype = content_type.split("/")
        mime = MIMEBase(maintype, subtype, filename=self._encode(file_name))
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=self._encode(file_name))
        # 把附件的内容读进来:
        mime.set_payload(content)
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        # msg.attach(mime)
        return mime

    def send_email(self, subject, text, file_name=None, content=None):
        # content = utf8(content) if content is not None else content
        msg = self._get_msg(subject)
        msg.attach(MIMEText(text, self.msg_type, self.encoding))
        if content is not None:
            msg.attach(self._send_file(file_name, content))
        self._send_email(msg)


class Email(BaseEmail):
    def __init__(self, to_addr, msg_type):
        BaseEmail.__init__(self, to_addr, msg_type)


@app.task
def send_email(to_addr, msg_type, subject, text, **kwargs):
    Email(to_addr, msg_type).send_email(subject, text, **kwargs)
