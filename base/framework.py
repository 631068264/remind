#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/16 13:59
@annotation = '' 
"""
import json

from attrdict import AttrDict
from base import util
from tornado.escape import json_decode
from tornado.web import url, RequestHandler


class Route:
    """
    Usage:

    route = RouteCollector('remind', prefix='/android_push')


    @route("/main")
    class MainHandler(RequestHandler):
        def get(self, *args, **kwargs):
            self.write("Hello world")

    ...

    app = Application()
    route.add_to_router(app.router)

    In the template use "url('reverse_route_name')" to get the url
    """

    def __init__(self, path, handler, name=None, **kwargs):
        self.path = path
        self.handler = handler
        self.name = name
        self.kwargs = kwargs

    def add_router(self, prefix=''):
        router = url(r'' + prefix + self.path, self.handler, name=self.name, **self.kwargs)
        return router


class RouteCollector(list):
    """
    Usage :
        RouteCollector should have a name
    """

    def __init__(self, name='', prefix='', routes=[]):
        if not name:
            raise Exception("RouteCollector should have a name")
        if prefix and not prefix.startswith("/"):
            raise Exception("RouteCollector prefix startswith / ")

        list.__init__(self, routes)
        self._prefix_path = prefix
        self._prefix_name = name

    def __call__(self, path, name=None, **kwargs):
        self._method_name = name

        def wrapper(handler):
            if self._method_name:
                reverse_route_name = r'%s.%s' % (self._prefix_name, self._method_name)
            else:
                reverse_route_name = r'%s.%s' % (self._prefix_name, handler.__name__.split("Handler")[0])
                reverse_route_name = util.camel_to_underline(reverse_route_name, ".")
            self.append(Route(path, handler, name=reverse_route_name, **kwargs))
            return handler

        return wrapper

    def add_router(self, prefix=''):
        router_list = []
        for route in self:
            router_list.append(route.add_router(prefix=prefix + self._prefix_path))
        return router_list


class BaseHandler(RequestHandler):
    def on_finish(self):
        print("on_finish")

    def prepare(self):
        self.safe_vars = {}
        if self.request.query_arguments:
            for query_name in self.request.query_arguments.keys():
                self.safe_vars[query_name] = self.get_query_argument(query_name)
        if self.request.body_arguments:
            for query_name in self.request.body_arguments.keys():
                self.safe_vars[query_name] = self.get_body_argument(query_name)
        if "application/json" == self.request.headers.get("Content-Type"):
            self.safe_vars = json_decode(self.request.body)
        if self.safe_vars:
            self.safe_vars = AttrDict(self.safe_vars)

    def write_json(self, is_ok=True, msg="", **kwargs):
        response = {
            "status": 1 if is_ok else 0,
            "msg": msg,
        }
        if kwargs:
            response.update(kwargs)
        self.write(json.dumps(response))
