import argparse
import os
import subprocess

from .settings import configuration, FILENAME_GENERATOR, FILE_HEADER_GENERATOR, SUBCOMMAND_PREFIX

def take(cli_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='Title or topic of notes file (in slug format)', type=str)

    args = parser.parse_args(cli_args)

    filename = os.path.join(configuration['NOTES_SOURCE_DIR'], FILENAME_GENERATOR(args.title))

    with open(filename, 'a') as fout:
        fout.write(FILE_HEADER_GENERATOR(args.title) + '\n')
    
    editor_command = [
        configuration['TEXT_EDITOR'],
        filename,
    ]

    print(SUBCOMMAND_PREFIX, ' '.join(editor_command))
    subprocess.call(editor_command)
