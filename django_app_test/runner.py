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
    are using Python 2.6 it will just work out of the box for you.
    """
    parser = OptionParser()
    parser.add_option("--DATABASE_ENGINE", dest="DATABASE_ENGINE", default="django.db.backends.sqlite3")
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
                'ENGINE': options.DATABASE_ENGINE,
                'NAME': options.DATABASE_NAME, #':memory:',
                'USER': options.DATABASE_USER,
                'PASSWORD': options.DATABASE_PASSWORD,
                'HOST': '',
                'PORT': '',
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

        # Force test runner to be the pre django 1.6 test runner. This tool does not work with then new default in 1.6.
        "TEST_RUNNER": "django.test.simple.DjangoTestSuiteRunner"
    })
    call_command("test", app_name)

if __name__ == "__main__":
    main()
