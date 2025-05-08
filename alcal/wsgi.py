"""
WSGI config for alcal project.

It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
#from django.core.wsgi import get_wsgi_application
#

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alcal.settings")  
application = get_wsgi_application()  
application = WhiteNoise(application)