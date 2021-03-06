import subprocess

from .settings import configuration, MAKEFILE_LOCATION

def _get_make_variables():
    return {
        'NOTES_SOURCE_DIR' : configuration['NOTES_SOURCE_DIR'],
        'NOTES_OUTPUT_DIR' : configuration['NOTES_OUTPUT_DIR'],
        'GUIDE_FILENAME' : configuration['GUIDE_FILENAME'],
        'NOTE_COMPILER' : 'notes compile -o {}'.format(configuration['NOTES_OUTPUT_DIR']),
        'GUIDE_COMPILER' : 'notes guide -o {} {}'.format(configuration['NOTES_OUTPUT_DIR'], configuration['GUIDE_FILENAME']),
    }

def compile_all(cli_args):
    _make(cli_args)


def clean(cli_args):
    _make(cli_args, additional_args=['clean'])


def _make(cli_args, additional_args=[]):
    MAKEFILE_VARIABLES = _get_make_variables()

    make_variables = [str(key) + '=' + str(MAKEFILE_VARIABLES[key]) for key in MAKEFILE_VARIABLES]

    make_command = [
        'make',
        '-f', MAKEFILE_LOCATION,
    ] + make_variables + additional_args

    print(' '.join(make_command))
    subprocess.call(make_command)
