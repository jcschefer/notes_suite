import argparse
import os
import pathlib
import subprocess

from .settings import configuration, SUBCOMMAND_PREFIX

def compiler(cli_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--preview', help='preview the file without saving the output', action='store_true')
    parser.add_argument('-o', '--output-dir', help='output directory to prefix file names with', type=str, default='.')
    parser.add_argument('filename', help='Markdown file to be compiled', type=str)
    args = parser.parse_args(cli_args)

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
        configuration['PDF_COMPILER'],
        '-t', 'latex',
        '-V', 'geometry:margin=1in',
        '-o', outfile_name,
        args.filename
    ]

    print(SUBCOMMAND_PREFIX, ' '.join(pdf_compilation_command))
    subprocess.call(pdf_compilation_command)

    if args.preview:
        view_command = [
            configuration['PDF_VIEWER'],
            outfile_name
        ]

        print(SUBCOMMAND_PREFIX, ' '.join(view_command))
        subprocess.call(view_command)
        print(SUBCOMMAND_PREFIX, 'removing', outfile_name)
        os.remove(outfile_name)
