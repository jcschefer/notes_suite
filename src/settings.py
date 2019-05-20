import json
import pathlib
import os

from datetime import datetime

# User Defined Constants (defaults)
configuration = {
    'NOTES_SOURCE_DIR' : 'src',
    'NOTES_OUTPUT_DIR' : 'build',
    'GUIDE_FILENAME' : 'guide.pdf',
   
    'PDF_COMPILER' : 'pandoc',
    'PDF_VIEWER' : 'zathura',
    'TEXT_EDITOR' : 'vim',
    
    'FILE_HEADER_FORMAT_STR' : '%B %d',
    'FILENAME_FORMAT_STR' : '%b-%d',
    'EXPECTED_DATE_FORMAT_LEN' : 6,
}

# Miscellaneous settings

SUBCOMMAND_PREFIX = '\t->'

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
MAKEFILE_LOCATION = os.path.join(SCRIPT_DIRECTORY, 'Makefile-notes')

FILENAME_GENERATOR = lambda title: datetime.strftime(datetime.now(), configuration['FILENAME_FORMAT_STR']).lower() + '-' + title + '.md'
FILE_HEADER_GENERATOR = lambda title: '# ' + datetime.strftime(datetime.now(), configuration['FILE_HEADER_FORMAT_STR']) + ': ' + title
FILENAME_SORTER = lambda fname: datetime.strptime(fname[:configuration['EXPECTED_DATE_FORMAT_LEN']], configuration['FILENAME_FORMAT_STR'])

def parse_settings():
    try:
        config_path = pathlib.Path('notes.json')
        with config_path.open() as config_file:
            config = json.load(config_file)
            for key in config.keys():
                configuration[key] = config[key]
                
    except FileNotFoundError:
        print('The current directory is not configured as a notes project')
        print('To create a default configuration, consider running:')
        print('$ notes generate')
        exit(1)

def generate_config(cli_args):
    print('creating notes.json file for use as notes project')
    with open('notes.json', 'w') as config_file:
        config_file_lines = [
            '{',
            '\t"comments": "These settings determine project directory structure, all paths are relative from project root",',
            '\t"NOTES_SOURCE_DIR": "src",',
            '\t"NOTES_OUTPUT_DIR": "build",',
            '\t"GUIDE_FILENAME": "guide.pdf",',
            '',
            '\t"comments": "These settings deal with how you would like filenames and auto-generated top headlines to read",',
            '\t"FILENAME_FORMAT_STR": "%b-%d",',
            '\t"FILE_HEADER_FORMAT_STR": "%B %d",',
            '\t"EXPECTED_DATE_FORMAT_LEN": 6,',
            '',
            '\t"comments": "These settings deal with the shell commands that will be used for the project",',
            '\t"PDF_VIEWER": "zathura",',
            '\t"TEXT_EDITOR": "vim",',
            '\t"PDF_COMPILER": "pandoc"',
            '}',
        ]

        config_file.write('\n'.join(config_file_lines))

    print('To update project settings, edit the notes.json file')
