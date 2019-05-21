#!/usr/bin/python3

import argparse
import os
import subprocess
import sys

from .compiler import compiler
from .guide import guide
from .make import clean, compile_all
from .take import take
from .settings import generate_config, parse_settings


def not_implemented(args):
    print('Invalid command or not implemented...')

supported_commands = {
    None : compile_all,
    'clean' : clean,
    'compile' : compiler,
    'generate' : generate_config,
    'guide' : guide,
    'take' :  take,
}

def help_msg():
    return '''notes [command]
    <none>          compile all updated Markdown files in the source directory
    clean           remove all compiled PDFs from the output directory
    compile         compile a single specified Markdown file
    generate        generate a default configuration file for a notes project
    guide           build a single guide from all compiled PDFs
    take            begin a new day of notes
    '''

def main():
    parser = argparse.ArgumentParser(description='A command-line based notes suite', usage=help_msg())
    parser.add_argument('command', nargs='?', help='command to run')
    args = parser.parse_args(sys.argv[1:2])

    func = supported_commands.get(args.command, not_implemented)

    if func != generate_config:
        parse_settings()

    func(sys.argv[2:])
