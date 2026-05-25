import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'BlogWebsite.settings'

import sys
print("SETTINGS MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'), file=sys.stderr)
print("PYTHON PATH:", sys.path, file=sys.stderr)

application = get_wsgi_application()