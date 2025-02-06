import os
import pytest
from unittest.mock import patch
import src.__init__ as env
from src.config.restart_system import run
from tests import remove_files, is_restarted_system

@pytest.fixture
def restart_system():
    remove_files()
    env.load_file_env(True)
    yield
    remove_files()


# testa restaurar o sistema manualmmente
def test_restart_system_manually(restart_system):
    assert not is_restarted_system() # garante que o sistema está normalmente

    env.set_env(BOT_NAME = 'TESTING')

    assert env.BOT_NAME == 'TESTING'

    with patch('builtins.input', return_value='RESTART SYSTEM'):
        restartion = run(env) # restarta o sistema

        assert env.BOT_NAME == 'CryptoSentinel'


# testa restaurar o sistema manualmmente
def test_restart_system_automatically(restart_system):
    assert not is_restarted_system() # garante que o sistema está normalmente

    env.set_env(BOT_NAME = 'TESTING')

    assert env.BOT_NAME == 'TESTING'

    with patch('builtins.input', return_value=''):
        restartion = run(env, autoconfirm=True) # restarta o sistema

        assert env.BOT_NAME == 'CryptoSentinel'


# testa restaurar o sistema com uma confirmação errada
def test_restart_system_manually_failure(restart_system):
    assert not is_restarted_system() # garante que o sistema está normalmente

    env.set_env(BOT_NAME = 'TESTING')

    assert env.BOT_NAME == 'TESTING'

    with patch('builtins.input', return_value='RESTART_SYSTEM'):
        restartion = run(env) # restarta o sistema

        assert env.BOT_NAME == 'TESTING'


# testa negar a restauração do sistema manualmmente
def test_restart_system_automatically_denies(restart_system):
    assert not is_restarted_system() # garante que o sistema está normalmente

    env.set_env(BOT_NAME = 'TESTING')

    assert env.BOT_NAME == 'TESTING'

    with patch('builtins.input', return_value=''):
        restartion = run(env, autoden=True) # restarta o sistema

        assert env.BOT_NAME == 'TESTING'