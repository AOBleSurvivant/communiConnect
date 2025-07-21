import os
import sys

# Add the project directory to the sys.path
path = '/home/yourusername/communiConnect/backend'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'communiconnect.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 