from __future__ import absolute_import

from iface.settings.base import *
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# Default is local environment
environment = os.getenv('DJANGO_SETTINGS_MODULE', 'local')


if environment.endswith('production'):
    print(34)
    from .production import *
