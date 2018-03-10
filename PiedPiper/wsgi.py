"""
WSGI config for PiedPiper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.path.exists('/etc/cryptopiper/settings.py'):
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "/etc/cryptopiper/settings.py")
    except ModuleNotFoundError:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PiedPiper.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PiedPiper.settings")

application = get_wsgi_application()
