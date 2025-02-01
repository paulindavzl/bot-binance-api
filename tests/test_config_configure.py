import os
import pytest
from unittest.mock import patch
import src.__init__ as env
from src.config.configure import start
from utils import remove_files


@pytest.fixture
def restart_system():
    remove_files()
    env.load_file_env(True)
    yield
    remove_files()


@pytest.fixture
def commands() -> dict:
    cmds = {'--name': 'BOT_NAME', '--adm': 'ADM', '--github': 'GITHUB', '--lang': 'LANG', '--debug': 'DEBUG', '--user': 'DB_USER', '--host': 'DB_HOST', '--port': 'DB_PORT', '--pass': 'DB_PASSWORD', '--dbname': 'DB_NAME', '--accesskey': 'ACCESS_KEY', '--secretkey': 'SECRET_KEY', '--timekey': 'TIME_CHANGE_KEY', '--timebackup': 'TIME_CHANGE_BACKUP_KEY'}
    return cmds


# testa todos o comandos confirmando manualmente
def test_all_commands_manually_confirmation(restart_system, commands):
    for cmd, tcmd in commands.items():
        if cmd == '--debug': test_value = 'off'
        elif cmd == '--lang': test_value = 'en'
        else: test_value = 'test_value'

        cmd_line = f'{cmd} {test_value}'
        resp = [cmd_line, 'y', 'exit']

        with patch('builtins.input', side_effect=resp):
            with pytest.raises(SystemExit):
                start()

            result = env.get_env(tcmd)

            if tcmd == 'DEBUG': assert not result
            else: assert result == test_value


# testa todos o comandos confirmando automaticamente
def test_all_commands_automatically_confirmation(restart_system, commands):
    for cmd, tcmd in commands.items():
        if cmd == '--debug': test_value = 'off'
        elif cmd == '--lang': test_value = 'en'
        else: test_value = 'test_value'

        cmd_line = f'{cmd} {test_value} -y'
        resp = [cmd_line, 'exit']

        with patch('builtins.input', side_effect=resp):
            with pytest.raises(SystemExit):
                start()

            result = env.get_env(tcmd)

            if tcmd == 'DEBUG': assert not result
            else: assert result == test_value

        
# testa todos o comandos confirmando manualmente
def test_all_commands_manually_denial(restart_system, commands):
    for cmd, tcmd in commands.items():
        if cmd == '--debug': test_value = 'off'
        elif cmd == '--lang': test_value = 'en'
        else: test_value = 'test_value'

        cmd_line = f'{cmd} {test_value}'
        resp = [cmd_line, 'n', 'exit']

        with patch('builtins.input', side_effect=resp):
            with pytest.raises(SystemExit):
                start()

            result = env.get_env(tcmd)

            if tcmd == 'DEBUG': assert result
            else: assert result != test_value


# testa todos o comandos confirmando automaticamente
def test_all_commands_automatically_denial(restart_system, commands):
    for cmd, tcmd in commands.items():
        if cmd == '--debug': test_value = 'off'
        elif cmd == '--lang': test_value = 'en'
        else: test_value = 'test_value'

        cmd_line = f'{cmd} {test_value} -n'
        resp = [cmd_line, 'exit']

        with patch('builtins.input', side_effect=resp):
            with pytest.raises(SystemExit):
                start()

            result = env.get_env(tcmd)

            if tcmd == 'DEBUG': assert result
            else: assert result != test_value


# testa executar vários comandos de uma vez confirmando automaticamente
def test_several_commands_automatically_confirmation(restart_system):
    cmd_line = '--user user_test --host 0.0.0.0 --port 5000 -y'
    resp = [cmd_line, '', '','exit']

    with patch('builtins.input', side_effect=resp):
        with pytest.raises(SystemExit):
            start()
    
    assert env.DB_USER == 'user_test'
    assert env.DB_HOST == '0.0.0.0'
    assert env.DB_PORT == 5000


# testa executar vários comandos de uma vez confirmando manualmente
def test_several_commands_manually_confirmation(restart_system):
    cmd_line = '--user user_test --host 0.0.0.0 --port 5000'
    resp = [cmd_line, 'y', '', 'y', '', 'y','exit']

    with patch('builtins.input', side_effect=resp):
        with pytest.raises(SystemExit):
            start()
    
    assert env.DB_USER == 'user_test'
    assert env.DB_HOST == '0.0.0.0'
    assert env.DB_PORT == 5000


# testa vários comandos de uma vez negando todos automaticamente
def test_several_commands_automatically_denial(restart_system):
    cmd_line = '--user user_test --host 0.0.0.0 --port 5000 -n'
    resp = [cmd_line, '','exit']

    with patch('builtins.input', side_effect=resp):
        with pytest.raises(SystemExit):
            start()
    
    assert env.DB_USER == 'root'
    assert env.DB_HOST == 'localhost'
    assert env.DB_PORT == 3306


# testa executar vários comandos de uma vez confirmando manualmente
def test_several_commands_manually_confirmation(restart_system):
    cmd_line = '--user user_test --host 0.0.0.0 --port 5000'
    resp = [cmd_line, 'n', '', 'n', '', 'n', 'exit']

    with patch('builtins.input', side_effect=resp):
        with pytest.raises(SystemExit):
            start()
    
    assert env.DB_USER == 'root'
    assert env.DB_HOST == 'localhost'
    assert env.DB_PORT == 3306