#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/16 13:17
@annotation = '' 
"""
import os
import views

from tornado.ioloop import IOLoop
from tornado.web import Application

if __name__ == '__main__':
    handler = []
    for view_name in views.__all__:
        module = __import__('views.%s' % view_name, fromlist=[view_name])
        handler.extend(module.route.add_router())

    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        # xsrf_cookies=True,
        # login_url="/auth/login",
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        debug=True,
    )
    app = Application(handler, **settings)
    app.listen(8888)
    IOLoop.current().start()
