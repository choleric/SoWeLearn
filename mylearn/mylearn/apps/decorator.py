from functools import wraps
from django.utils import html

def html_entity_encode():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            source = None
            if "GET" == request.method :
                source = "GET"
            elif "POST" == request.method :
                source = "POST"

            if None != source :
                params = getattr(request, source).copy()
                for k,v in params.iteritems() :
                    if isinstance(v, basestring) :
                        params[k] = html.escape(v)

                setattr(request, source, params)
            return func(request, *args, **kwargs)

        return wraps(func)(inner_decorator)

    return decorator
