from __future__ import absolute_import, unicode_literals
import speckenv
import os
from django.core.wsgi import get_wsgi_application

speckenv.read_speckenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkweb.settings")
application = get_wsgi_application()
