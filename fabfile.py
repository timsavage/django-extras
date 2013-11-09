# Use fabric to automate some stuff
from fabric.api import *

def run_tests():
    local('python -mdjango_app_test.runner django_extras')
