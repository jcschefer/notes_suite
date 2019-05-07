import argparse
import os
import subprocess
import sys

from .settings import *

def take():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='Title or topic of notes file (in slug format)', type=str)

    args = parser.parse_args(sys.argv[SUBPARSER_ARGV_START_INDEX:])

    filename = os.path.join(NOTES_SOURCE_DIR, FILENAME_GENERATOR(args.title))

    with open(filename, 'w') as fout:
        fout.write(FILE_HEADER_GENERATOR(args.title) + '\n')
    
    editor_command = [
        TEXT_EDITOR,
        filename,
    ]

    print(SUBCOMMAND_PREFIX, ' '.join(editor_command))
    subprocess.call(editor_command)
