from os import getcwd
from os.path import join, isfile, getsize

from apio.commands.init import cli as cmd_init


def validate_apio_ini(current_dir):
    path = join(current_dir, 'apio.ini')
    assert isfile(path) and getsize(path) > 0


def validate_scons(apioproject_dir):
    path = join(apioproject_dir, 'SConstruct')
    assert isfile(path) and getsize(path) > 0


def test_init_default(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():
        result = clirunner.invoke(cmd_init)
        validate_cliresult(result)


def test_init_board(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():
        result = clirunner.invoke(cmd_init, ['--board', 'icezum'])
        validate_cliresult(result)
        validate_apio_ini(getcwd())
        assert 'apio.ini file created' in result.output


def test_init_scons(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():

        # apio init --scons
        result = clirunner.invoke(cmd_init, ['--scons'])
        validate_cliresult(result)
        validate_scons(getcwd())
        assert 'Creating SConstruct file ...' in result.output
        assert 'has been successfully created!' in result.output

        # apio init --scons
        result = clirunner.invoke(cmd_init, ['--scons'], input='y')
        validate_cliresult(result)
        validate_scons(getcwd())
        assert 'Warning' in result.output
        assert 'file already exists' in result.output
        assert 'Do you want to replace it?' in result.output
        assert 'has been successfully created!' in result.output