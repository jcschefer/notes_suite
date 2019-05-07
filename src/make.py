import subprocess

from .settings import *

def compile_all():
    make()


def clean():
    make(additional_args=['clean'])


def make(additional_args=[]):
    make_variables = [str(key) + '=' + str(MAKEFILE_VARIABLES[key]) for key in MAKEFILE_VARIABLES]

    make_command = [
        'make',
        '-f', MAKEFILE_LOCATION,
    ] + make_variables + additional_args

    print(' '.join(make_command))
    subprocess.call(make_command)
