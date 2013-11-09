#!/usr/bin/env python

import os
import sys

from optparse import OptionParser

from django.conf import settings
from django.core.management import call_command

def main():
    """
    The entry point for the script. This script is fairly basic. Here is a
    quick example of how to use it::

        app_test_runner.py [path-to-app]

    You must have Django on the PYTHONPATH prior to running this script. This
    script basically will bootstrap a Django environment for you.

    By default this script with use SQLite and an in-memory database. If you
    are using Python 2.5 it will just work out of the box for you.

    TODO: show more options here.
    """
    parser = OptionParser()
    parser.add_option("--DATABASE_ENGINE", dest="DATABASE_ENGINE", default="sqlite3")
    parser.add_option("--DATABASE_NAME", dest="DATABASE_NAME", default="")
    parser.add_option("--DATABASE_USER", dest="DATABASE_USER", default="")
    parser.add_option("--DATABASE_PASSWORD", dest="DATABASE_PASSWORD", default="")
    parser.add_option("--SITE_ID", dest="SITE_ID", type="int", default=1)

    options, args = parser.parse_args()

    # check for app in args
    try:
        app_path = args[0]
    except IndexError:
        print("You did not provide an app path.")
        raise SystemExit
    else:
        if app_path.endswith("/"):
            app_path = app_path[:-1]
        parent_dir, app_name = os.path.split(app_path)
        sys.path.insert(0, parent_dir)

    settings.configure(**{
        "DATABASES": {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': ':memory:',                      # Or path to database file if using sqlite3.
                'USER': '',                      # Not used with sqlite3.
                'PASSWORD': '',                  # Not used with sqlite3.
                'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            }
        },
        "SITE_ID": options.SITE_ID,
        "SECRET_KEY": "Test Key",
        "ROOT_URLCONF": "django_app_test.urls",
        "TEMPLATE_LOADERS": (
            "django.template.loaders.app_directories.Loader",
        ),
        "TEMPLATE_DIRS": tuple(),
        "INSTALLED_APPS": (
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            app_name,
        ),
        "TEST_RUNNER": "django.test.simple.DjangoTestSuiteRunner"
    })
    call_command("test", app_name)

if __name__ == "__main__":
    main()
