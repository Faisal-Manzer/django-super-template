"""
Defines root level sub-domain separation based on type of API Interface
"""

from django_hosts import patterns, host


host_patterns = patterns(
    '',
    host(r'admin', '__config__.urls.admin', name='admin'),
    host(r'api', '__config__.urls.api', name='api'),
    host(r'', '__config__.urls', name='default'),
)
