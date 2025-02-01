import pytest
from unittest.mock import patch
import src.__init__ as env
from src.config.execute_comands import Execute
from utils import remove_files


@pytest.fixture
def restart_system():
    remove_files()
    env.load_file_env(True)
    yield 
    remove_files()


# testa executar um comando com confirmação manual
def test_execute_manual_confirmation(restart_system):
    assert env.DB_USER == 'root' # confirma o valor de DB_USER antes do teste

    cmd = {'--user': 'test', '-y': False, '-n': False}
    response = '--user test'
    execute = Execute
    with patch('builtins.input', return_value='y'):
        execute = Execute(cmd, env, response)

    assert execute.executed == ['--user']
    assert env.DB_USER == 'test' # confirma que o comando foi executado


# testa executar um comando com negação manual
def test_execute_manual_denial(restart_system):
    assert env.DB_USER == 'root' # confirma o valor de DB_USER antes do teste

    cmd = {'--user': 'test', '-y': False, '-n': False}
    response = '--user test'
    execute = Execute
    with patch('builtins.input', return_value='n'):
        execute = Execute(cmd, env, response)

    assert execute.executed is None
    assert env.DB_USER == 'root' # confirma que o comando não foi executado


# testa executar um comando com confirmação automática
def test_execute_auto_confirmation(restart_system):
    assert env.DB_USER == 'root' # confirma o valor de DB_USER antes do teste

    cmd = {'--user': 'test', '-y': True, '-n': False}
    response = '--user test -y'
    execute = Execute
    with patch('builtins.input', return_value=''):
        execute = Execute(cmd, env, response)

    assert execute.executed == ['--user']
    assert env.DB_USER == 'test' # confirma que o comando foi executado


# testa executar um comando com confirmação automática
def test_execute_auto_denial(restart_system):
    assert env.DB_USER == 'root' # confirma o valor de DB_USER antes do teste

    cmd = {'--user': 'test', '-y': False, '-n': True}
    response = '--user test -n'
    execute = Execute
    with patch('builtins.input', return_value=''):
        execute = Execute(cmd, env, response)

    assert execute.executed is None
    assert env.DB_USER == 'root' # confirma que o comando foi executado


# testa executar --restart_system manualmente
def test_execute_restart_system_manual(restart_system):
    env.set_env(DB_USER = 'test') # altera DB_USER

    cmd = {'--restart_system': True, '-y':  False, '-n': False}
    response = '--restart_system'
    execute = Execute
    with patch('builtins.input', return_value='RESTART SYSTEM'):
        execute = Execute(cmd, env, response)

    assert execute.executed == ['--restart_system']
    assert env.DB_USER == 'root' # confirma que DB_USER voltou para padrão


# testa executar o comando --debug
def test_execute_debug(restart_system):
    assert env.DEBUG

    cmd = {'--debug': 'off', '-y': True, '-n': False}
    response = '--debug off'
    execute = Execute
    with patch('builtins.input', return_value=''):
        execute = Execute(cmd, env, response)

    assert execute.executed == ['--debug']
    assert not env.DEBUG # confirma que DEBUG foi desativado

    cmd = {'--debug': 'on', '-y': True, '-n': False}
    response = '--debug on'
    execute = Execute
    with patch('builtins.input', return_value=''):
        execute = Execute(cmd, env, response)

    assert execute.executed == ['--debug']
    assert env.DEBUG # confirma que DEBUG foi ativado