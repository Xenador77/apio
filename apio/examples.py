# Execute functions

import os
import glob
import click
import shutil

from os.path import join, isdir, isfile, dirname, basename


# -- Error messages
EXAMPLE_NOT_FOUND_MSG = """
Warning: this example does not exist
Use `apio examples -l` for listing all the available examples"""

EXAMPLE_OF_USE_CAD = """
Example of use:
   apio examples -f leds
Copy the leds example files to the current directory"""

EXAMPLE_DIR_FILE = """
To get an example, use the command:
   apio examples -d/-f name"""


class Examples(object):

    def __init__(self):
        self.examples_dir = join(dirname(__file__), '..', 'examples')

    def list_examples(self):
        examples = sorted(os.listdir(self.examples_dir))
        click.secho('')
        for example in examples:
            example_dir = join(self.examples_dir, example)
            info_path = join(example_dir, 'info')
            info = ''
            if isfile(info_path):
                with open(info_path, 'r') as info_file:
                    info = info_file.read().replace('\n', '')
            click.secho(' ' + example, fg='blue', bold=True)
            click.secho('-' * click.get_terminal_size()[0])
            click.secho(' ' + info)
            click.secho('')
        click.secho(EXAMPLE_DIR_FILE, fg='green')
        click.secho(EXAMPLE_OF_USE_CAD, fg='green')
        return

    def copy_example_dir(self, example):
        example_path = join(os.getcwd(), example)
        local_example_path = join(self.examples_dir, example)

        if isdir(local_example_path):
            if isdir(example_path):
                click.secho(
                    'Warning: ' + example + ' directory already exists',
                    fg='yellow')
                if click.confirm('Do you want to replace it?'):
                    shutil.rmtree(example_path)
                    self._copy_dir(example, local_example_path, example_path)
            elif isfile(example_path):
                click.secho(
                    'Warning: ' + example + ' is already a file', fg='yellow')
            else:
                self._copy_dir(example, local_example_path, example_path)
        else:
            click.secho(EXAMPLE_NOT_FOUND_MSG, fg='yellow')

    def copy_example_files(self, example):
        example_path = os.getcwd()
        local_example_path = join(self.examples_dir, example)

        if isdir(local_example_path):
            self._copy_files(example, local_example_path, example_path)
        else:
            click.secho(EXAMPLE_NOT_FOUND_MSG, fg='yellow')

    def _copy_files(self, example, src_path, dest_path):
        click.secho('Copying ' + example + ' example files ...')
        example_files = glob.glob(join(src_path, '*'))
        for f in example_files:
            filename = basename(f)
            if filename != 'info':
                if isfile(join(dest_path, filename)):
                    click.secho(
                        'Warning: ' + filename + ' file already exists',
                        fg='yellow')
                    if click.confirm('Do you want to replace it?'):
                        shutil.copy(f, dest_path)
                elif isdir(join(dest_path, filename)):
                    click.secho(
                        'Warning: ' + filename + ' is already a directory',
                        fg='yellow')
                    return
                else:
                    shutil.copy(f, dest_path)
        click.secho(
            'Example files \'' + example + '\' have been successfully created!',
            fg='green')

    def _copy_dir(self, example, src_path, dest_path):
        click.secho('Creating ' + example + ' directory ...')
        shutil.copytree(src_path, dest_path)
        click.secho(
            'Example \'' + example + '\' has been successfully created!',
            fg='green')

    def examples_of_use_cad(self):
        return EXAMPLE_OF_USE_CAD