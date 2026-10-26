"""
ASGI config for proyecto_config project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_config.settings')
application = get_asgi_application()
