import os
from setuptools import setup, find_packages


# Hack to force dist utils to install data files in correct location along with
# Python package.
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""


def full_split(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return full_split(head, [tail] + result)

# Compile the list of data files available.
data_files = []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
for dir_path, dir_names, file_names in os.walk('django_extras'):
    # Ignore .directories and Python3 cache directories
    for idx, dir_name in enumerate(dir_names):
        if dir_name.startswith('.') or dir_name == '__pycache__':
            del dir_names[idx]

    # Ignore package directories
    if '__init__.py' in file_names:
        continue
    elif file_names:
        data_files.append([dir_path, [os.path.join(dir_path, f) for f in file_names]])


setup(
    name='django-extras',
    version='0.3',
    url="https://github.com/timsavage/django-extras",
    license='LICENSE',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='Object Data Mapping for Python',
    long_description=long_description,
    packages=find_packages(exclude=('django_app_test',)),
    data_files=data_files,
    install_requires=['django>=1.4', 'six'],
    zip_safe=False,

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
