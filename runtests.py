import os, sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG=True, INSTALLED_APPS=('django_extras'))

from django.test.simple import run_tests

failures = run_tests(['django_extras',], verbosity=1)
if failures:
    sys.exit(failures)
