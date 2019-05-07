import os

from datetime import datetime

SUBCOMMAND_PREFIX = '\t->'
SUBPARSER_ARGV_START_INDEX = 2

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
MAKEFILE_LOCATION = os.path.join(SCRIPT_DIRECTORY, 'Makefile-notes')

NOTES_SOURCE_DIR = 'src'
NOTES_OUTPUT_DIR = 'build'
GUIDE_FILENAME = 'guide.pdf'

MAKEFILE_VARIABLES = {
    'NOTES_SOURCE_DIR' : NOTES_SOURCE_DIR,
    'NOTES_OUTPUT_DIR' : NOTES_OUTPUT_DIR,
    'GUIDE_FILENAME' : GUIDE_FILENAME,
    'NOTE_COMPILER' : 'notes compile -o {}'.format(NOTES_OUTPUT_DIR),
    'GUIDE_COMPILER' : 'notes guide -o {} {}'.format(NOTES_OUTPUT_DIR, GUIDE_FILENAME),
}

FILENAME_GENERATOR = lambda title: datetime.strftime(datetime.now(), '%b-%d').lower() + '-' + title + '.md'
FILE_HEADER_GENERATOR = lambda title: datetime.strftime(datetime.now(), '%B %d') + ':' + title
FILENAME_SORTER = lambda fname: datetime.strptime(fname[:6], '%b-%d')

PDF_COMPILER = 'pandoc'
PDF_VIEWER = 'zathura'
TEXT_EDITOR = 'vim'
