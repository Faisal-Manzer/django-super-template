"""Contains overrides for some django default classes and functions"""

__all__ = ['ws_include']

from importlib import import_module

from channels.routing import URLRouter


def ws_include(arg, *_, **__):
    """Overrides include for websocket url to use `ws_urlpatterns` instead of `urlpatterns`."""

    if isinstance(arg, tuple):
        urlconf_module, _ = arg
    else:
        urlconf_module = arg

    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)

    urlconf_module = getattr(urlconf_module, 'ws_urlpatterns', urlconf_module)

    return URLRouter(urlconf_module)
