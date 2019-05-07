#!/usr/bin/python3

import argparse
import os
import pathlib
import subprocess
import sys

from datetime import datetime

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
MAKEFILE_LOCATION = os.path.join(SCRIPT_DIRECTORY, 'Makefile-notes')

SUBCOMMAND_PREFIX = '\t->'
SUBPARSER_ARGV_START_INDEX = 2

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

def main():
    supported_commands = {
        None : compile_all,
        'clean' : clean,
        'compile' : compiler,
        'guide' : guide,
        'take' :  take,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', help='command to run')
    args = parser.parse_args(sys.argv[1:SUBPARSER_ARGV_START_INDEX])

    func = supported_commands.get(args.command, not_implemented)
    func()


def not_implemented():
    print('Invalid command or not implemented...')


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


def compiler():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--preview', help='preview the file without saving the output', action='store_true')
    parser.add_argument('-o', '--output-dir', help='output directory to prefix file names with', type=str, default='.')
    parser.add_argument('filename', help='Markdown file to be compiled', type=str)
    args = parser.parse_args(sys.argv[SUBPARSER_ARGV_START_INDEX:])

    path = pathlib.Path(args.filename)
    pure_path = pathlib.PurePath(args.filename)

    if not path.is_file():
        print(SUBCOMMAND_PREFIX, 'file does not exist')
        exit(1)

    if not pure_path.suffix == '.md':
        print(SUBCOMMAND_PREFIX, 'must supply a Markdown file')
        exit(1)

    outfile_name = os.path.join(
        args.output_dir, 
        str(pure_path.stem) + '.pdf' if not args.preview else '.temp.pdf')

    pdf_compilation_command = [
        PDF_COMPILER,
        '-t', 'latex',
        '-V', 'geometry:margin=1in',
        '-o', outfile_name,
        args.filename
    ]

    print(SUBCOMMAND_PREFIX, ' '.join(pdf_compilation_command))
    subprocess.call(pdf_compilation_command)

    if args.preview:
        view_command = [
            PDF_VIEWER,
            outfile_name
        ]

        print(SUBCOMMAND_PREFIX, ' '.join(view_command))
        subprocess.call(view_command)
        print(SUBCOMMAND_PREFIX, 'removing', outfile_name)
        os.remove(outfile_name)
        

def guide():
    parser = argparse.ArgumentParser()
    parser.add_argument('guide_name', help='Target filename for guide file', type=str, default='guide.pdf')
    parser.add_argument('-o', '--output-dir', help='output directory to prefix file names with', type=str, default='.')
    parser.add_argument('-c', '--chronological', help='Organize files chronologically in time', action='store_true', default=False)

    args = parser.parse_args(sys.argv[SUBPARSER_ARGV_START_INDEX:])

    os.chdir(args.output_dir)

    if os.path.exists(args.guide_name):
        print(SUBCOMMAND_PREFIX, 'overwriting existing guide file...')
        os.remove(args.guide_name)

    path = pathlib.Path('.')
    files = [f.name for f in path.iterdir()]
    files.sort(reverse=(not args.chronological), key=FILENAME_SORTER)

    pdfunite_command = ['pdfunite'] + files + [args.guide_name]

    print(SUBCOMMAND_PREFIX, ' '.join(pdfunite_command))
    subprocess.call(pdfunite_command)

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
