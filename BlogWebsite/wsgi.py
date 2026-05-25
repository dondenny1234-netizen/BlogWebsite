import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogWebsite.settings')

django.setup()

# Run migrations at startup
from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=0)

application = get_wsgi_application()