# Helper test runner for running tests against django_extras
import os

from optparse import OptionParser

from django.conf import settings
from django.core.management import call_command

def main():
    parser = OptionParser()
    parser.add_option('--DATABASE_ENGINE', dest='DATABASE_ENGINE', default='sqlite3')
    parser.add_option('--DATABASE_NAME',   dest='DATABASE_NAME',   default='test.db')
    parser.add_option('--DATABASE_USER',   dest='DATABASE_USER',   default='')
    parser.add_option('--DATABASE_PASSWORD', dest='DATABASE_PASSWORD', default='')
    parser.add_option('--DATABASE_HOST',   dest='DATABASE_HOST',   default='')
    parser.add_option('--DATABASE_PORT',   dest='DATABASE_PORT',  default='')
    parser.add_option('--SITE_ID',         dest='SITE_ID', type='int', default=1)

    options, args = parser.parse_args()

    settings.configure(**{
        'DATABASES': {
            'default': {
                'ENGINE': options.DATABASE_ENGINE,
                'NAME': options.DATABASE_NAME,
                'USER': options.DATABASE_USER,
                'PASSWORD': options.DATABASE_PASSWORD,
                'HOST': options.DATABASE_HOST,
                'PORT': options.DATABASE_PORT,
            },
        },
        'SITE_ID': options.SITE_ID,
        'ROOT_URLCONF': '',
        'TEMPLATE_LOADERS': (
            'django.template.loaders.filesystem.load_template_source',
            'django.template.loaders.app_directories.load_template_source',
        ),
        'TEMPLATE_DIRS': (
            os.path.join(os.path.dirname(__file__), 'templates'),
        ),
        'INSTALLED_APPS': (
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",

            "django_extras",
        ),
    })
    call_command('test', 'django_extras', 'auth')


if __name__ == '__main__':
    main()
