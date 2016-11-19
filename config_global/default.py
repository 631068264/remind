#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/19 19:16
@annotation = '' 
"""


class PUSH_BULLET:
    HEADERS = {
        "Access-Token": "",
        "Content-Type": "application/json",
    }
    PHONE_ID = ""
    PC_ID = ""
    PUSH_URL = "https://api.pushbullet.com/v2/pushes"


class EMAIL:
    FROM_ADDR = ""
    PASSWORD = ""
    SMTP_SERVER = ""
    ENCONDING = "utf-8"


class TWILIO:
    ACCOUNT_SID = ""
    AUTH_TOKEN = ""
    FROM = ""
