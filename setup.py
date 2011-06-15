#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import join, dirname
import django_extras

if 'final' in django_extras.VERSION[-1]:
    CLASSIFIERS = ['Development Status :: 5 - Stable']
elif 'beta' in django_extras.VERSION[-1]:
    CLASSIFIERS = ['Development Status :: 4 - Beta']
else:
    CLASSIFIERS = ['Development Status :: 3 - Alpha']
CLASSIFIERS += [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name = "django-extras",
    version = django_extras.__version__,
    url = "https://bitbucket.org/timsavage/django-extras",
    author = "Tim Savage",
    author_email = "tim.savage@poweredbypenguins.org",
    license = "BSD License",
    description = "A selection of extra features for django that solve common annoyances and limitations.",
    long_description=open(join(dirname(__file__), 'README')).read(),
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    packages=find_packages(exclude=["example", "example.*"]),
    zip_safe = False,
)
