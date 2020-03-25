"""
Django configuration file per environment as described in `secrets.json`
"""


from __config__.secrets import SECRET

if SECRET['DJANGO']['DEBUG'] and not SECRET['DJANGO']['PRODUCTION']:
    from .development import *

# staging
elif SECRET['DJANGO']['DEBUG'] and SECRET['DJANGO']['PRODUCTION']:
    from .staging import *

# production
elif not SECRET['DJANGO']['DEBUG'] and SECRET['DJANGO']['PRODUCTION']:
    from .production import *
