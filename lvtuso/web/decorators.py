# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from functools import wraps
from django.http import HttpResponseBadRequest
from django.utils.decorators import available_attrs

def ajax_call(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return view_func(request, *args, **kwargs)

    return _wrapped_view
