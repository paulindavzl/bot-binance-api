import time
import pytest
import src.__init__ as env
from src.key_mechanism import default_mechanism_change_key, default_mechanism_get_key
from tests import remove_files

@pytest.fixture
def restart_system():
    remove_files()
    env.load_file_env(True)
    yield
    remove_files()


# testa alterar a chave
def test_default_mechanism_change_key(restart_system):
    # confirma o valor padrão das variáveis
    assert env.TIME_CHANGE_KEY == 3600.0
    assert env.TIME_CHANGE_BACKUP_KEY == 600.0

    env.set_env(TIME_CHANGE_KEY=2, TIME_CHANGE_BACKUP_KEY=0.5)# altera as variáveis para um valor viável à testes

    # confirma o valor das variáveis
    assert env.TIME_CHANGE_KEY == 2
    assert env.TIME_CHANGE_BACKUP_KEY == 0.5

    old_key = default_mechanism_get_key(env)
    old_backup_key = default_mechanism_get_key(env, backup=True)

    assert old_key == old_backup_key # confirma que as chaves são iguais

    default_mechanism_change_key(env) # altera as chaves

    new_key = default_mechanism_get_key(env)
    new_backup_key = default_mechanism_get_key(env, backup=True)

    assert new_key == new_backup_key # compara as novas chaves

    # compara as novas chaves com as antigas
    assert old_key != new_key
    assert old_backup_key != new_backup_key


# testa obter as chaves de decodificação
def test_defalut_mechanism_get_key(restart_system):
    # obtém as chaves
    old_key = default_mechanism_get_key(env)
    old_backup_key = default_mechanism_get_key(env, backup=True)

    # tenta obter as mesmas chaves
    new_key = default_mechanism_get_key(env)
    new_backup_key = default_mechanism_get_key(env, backup=True)

    # confirma que as chaves são iguais
    assert old_key == new_key
    assert old_backup_key == new_backup_key