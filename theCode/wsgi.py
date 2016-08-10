"""
WSGI config for proyecto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/ofployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
