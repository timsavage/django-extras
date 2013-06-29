# Use fabric to automate some stuff
from fabric.api import *

def run_tests():
    local('python -mtest_harness.runner')
