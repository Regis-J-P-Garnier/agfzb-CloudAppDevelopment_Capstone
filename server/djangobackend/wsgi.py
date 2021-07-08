"""
WSGI config for djangobackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
import os
from dotenv import load_dotenv

project_folder = os.path.expanduser(os.path.dirname(os.path.realpath(__file__)))  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '../djangobackend/.env'))
assert(os.getenv("DEBUG")=="True")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobackend.settings')

application = get_wsgi_application()
