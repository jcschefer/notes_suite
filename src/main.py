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
    'generate': generate_config,
    'guide' : guide,
    'take' :  take,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', help='command to run')
    args = parser.parse_args(sys.argv[1:2])

    func = supported_commands.get(args.command, not_implemented)

    if func != generate_config:
        parse_settings()

    func(sys.argv[2:])
