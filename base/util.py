#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2016/11/16 22:50
@annotation = '' 
"""


def camel_to_underline(camel, sep=''):
    '''''
        驼峰命名格式转下划线命名格式
    '''
    if not isinstance(camel, str):
        return ''

    def _camel_to_underline(camel):
        underline = camel[0].lower() if camel[0].isupper() else camel[0]

        for c in camel[1:]:
            underline += '_%s' % c.lower() if c.isupper() else c

        return underline

    upderline = ''
    camel_list = camel.split(sep)
    for camel in camel_list:
        upderline += _camel_to_underline(camel) + sep

    return upderline[:-len(sep)]


class WrapperByte(object):
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "WrapperByte"
