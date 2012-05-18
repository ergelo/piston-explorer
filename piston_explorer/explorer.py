from piston.handler import BaseHandler
from piston.doc import generate_doc

from django.core.urlresolvers import get_resolver, get_callable, get_script_prefix
from django.conf import settings as dj_settings

import settings
import inspect

def get_handlers():

    handler_path = '%s.%s' % (settings.API_MODULE, settings.API_HANDLER)
    handler_class = __import__(handler_path, fromlist = [settings.API_HANDLER])

    handlers = []
    for name, obj in inspect.getmembers(handler_class):
        if inspect.isclass(obj) and issubclass(obj, BaseHandler) and obj is not BaseHandler:
            uri = obj.resource_uri()
            doc = generate_doc(obj)

            if doc.resource_uri_template is None:
                urls = return_urls(obj)
            else:
                urls = [doc.resource_uri_template]

            handlers.append({'name': name, 'handler': obj, 'urls': urls})

    return handlers


def return_urls(handler):
    def _convert(template, params=[]):
        """URI template converter"""
        paths = template % dict([p, "{%s}" % p] for p in params)
        return u'%s%s' % (get_script_prefix(), paths)

    try:
        resource_uri = handler.resource_uri()
        components = [None, [], {}]
        for i, value in enumerate(resource_uri):
            components[i] = value

        lookup_view, args, kwargs = components
        lookup_view = get_callable(lookup_view, True)

        urls = []

        possibilities = get_resolver(None).reverse_dict.getlist(lookup_view)

        for possibility, pattern, empty in possibilities:
            for result, params in possibility:
                urls.append(_convert(result, params))

        return urls

    except:
        return None

