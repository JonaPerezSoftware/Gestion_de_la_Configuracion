"""
WSGI config for proyecto_config project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_config.settings')
application = get_wsgi_application()
