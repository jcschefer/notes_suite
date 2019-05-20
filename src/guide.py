import argparse
import os
import pathlib
import subprocess

from .settings import FILENAME_SORTER, SUBCOMMAND_PREFIX

def guide(cli_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('guide_name', help='Target filename for guide file', type=str, default='guide.pdf')
    parser.add_argument('-o', '--output-dir', help='output directory to prefix file names with', type=str, default='.')
    parser.add_argument('-c', '--chronological', help='Organize files chronologically in time', action='store_true', default=False)

    args = parser.parse_args(cli_args)

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
