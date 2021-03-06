#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/05 17:02:35


from __future__ import absolute_import

import functools
import inspect
import logging

from apps.utils.wsme import json
from django.shortcuts import HttpResponse

import wsme
import wsme.api
import wsme.rest.args
import wsme.rest.xml

from .handler import signature as _signature

log = logging.getLogger('apps')


TYPES = {
    'application/json': json,
    'application/xml': wsme.rest.xml,
    'text/xml': wsme.rest.xml
}


def get_dataformat(request):
    if 'Accept' in request:
        for t in TYPES:
            if t in request['Accept']:
                return TYPES[t]

    # Look for the wanted data format in the request.
    req_dataformat = getattr(request, 'content_type', None)
    if req_dataformat in TYPES:
        return TYPES[req_dataformat]

    log.info('''Could not determine what format is wanted by the
             caller, falling back to json''')
    return json


def signature(*args, **kw):
    sig = _signature(*args, **kw)

    def decorator(f):
        args = inspect.getfullargspec(f)[0]
        ismethod = args and args[0] == 'self'
        sig(f)
        funcdef = wsme.api.FunctionDefinition.get(f)
        # funcdef.resolve_types(wsme.types.registry)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if ismethod:
                self, args = args[0], args[1:]

            request, args = args[0], args[1:]
            # post的数据,request.body
            args, kwargs = wsme.rest.args.get_args(
                funcdef, args, kwargs,
                request.GET, {},
                request.body,
                request.content_type
            )
            
            dataformat = get_dataformat(request)
            try:
                # 常规路由fbv和django的类视图cbv
                result = f(request, *args, **kwargs) if not ismethod else f(self, request, *args, **kwargs)
                # result = f(*args, **kwargs)
                # NOTE: Support setting of status_code with default 200
                status_code = funcdef.status_code
                if isinstance(result, wsme.api.Response):
                    status_code = result.status_code
                    result = result.obj
                res = HttpResponse(dataformat.encode_result(
                    result,
                    funcdef.return_type
                ), content_type=dataformat.content_type, status=None if hasattr(result, 'code') else status_code)
            except Exception:
                raise
            return res
        wrapper.wsme_func = f
        return wrapper
    return decorator
