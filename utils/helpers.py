"""Helpers functions used by all apps"""


__all__ = ['get_uuid', 'consume_']


import uuid


def get_uuid():
    """Generates uuid random"""

    return str(uuid.uuid1())[:8]


def consume_(_):
    """Utility function to remove static waring"""
