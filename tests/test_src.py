import os
import re
import time
import pytest
import logging
from cryptography.fernet import InvalidToken
from dotenv import load_dotenv
import src.__init__ as env
from utils import remove_files


# apaga todos os logs, .key (backup.key), .enc e .env (não executar teste fora do contêiner Docker de testes [docker-compose testes])
@pytest.fixture
def restart_system():
    remove_files()

    env.load_file_env(True)

    yield

    remove_files()



# testa definir todas a variáveis para o padrão
def test_set_default_env(restart_system):
    env.set_env(DB_USER='test')
    
    assert env.DB_USER == 'test'

    # decodifica e limpa o arquivo .enc/.env
    env.decode_env()
    with open(env.PATH_ENV, 'w') as file:
        file.write('')
    env.encode_env()

    # define as variáveis para seus valores padrões
    env.set_default_env(True)
    env.load_file_env(True) # recarrega as variáveis

    assert env.DB_USER == 'root'
    assert env.DB_PASSWORD == 'Null'
    assert env.DB_NAME == 'database'
    assert env.DB_HOST == 'localhost'
    assert env.DB_PORT == 3306


# testa alterar a chave
def test_change_key(restart_system):
    # confirma o valor padrão das variáveis
    assert env.TIME_CHANGE_KEY == 3600.0
    assert env.TIME_CHANGE_BACKUP_KEY == 600.0

    env.set_env(TIME_CHANGE_KEY=2, TIME_CHANGE_BACKUP_KEY=0.5)# altera as variáveis para um valor viável à testes

    # confirma o valor das variáveis
    assert env.TIME_CHANGE_KEY == 2
    assert env.TIME_CHANGE_BACKUP_KEY == 0.5

    old_key = env.get_key()
    old_backup_key = env.get_key(backup=True)

    assert old_key == old_backup_key # confirma que as chaves são iguais

    env.change_key() # altera as chaves

    new_key = env.get_key()
    new_backup_key = env.get_key(backup=True)

    assert new_key == new_backup_key # compara as novas chaves

    # compara as novas chaves com as antigas
    assert old_key != new_key
    assert old_backup_key != new_backup_key


# testa obter as chaves de decodificação
def test_get_key(restart_system):
    # obtém as chaves
    old_key = env.get_key()
    old_backup_key = env.get_key(backup=True)

    # tenta obter as mesmas chaves
    new_key = env.get_key()
    new_backup_key = env.get_key(backup=True)

    # confirma que as chaves são iguais
    assert old_key == new_key
    assert old_backup_key == new_backup_key


# codifica/decodifica o arquivo .env
def test_decode_env_encode_env(restart_system):
    if os.path.exists(env.PATH_ENC):
        env.decode_env() # decodifica o arquivo .enc

    assert os.path.exists(env.PATH_ENV) # confirma que .enc foi decodificado
    assert not os.path.exists(env.PATH_ENC) # confirma que .enc foi excluído

    env.encode_env() # codifica o arquivo .env

    assert os.path.exists(env.PATH_ENC) # confirma que .env foi codificado

    assert not os.path.exists(env.PATH_ENV) # confirma .env foi excluído


# tenta decodificar o arquivo com uma chave inválida
def test_decode_env_invalid_token(restart_system):
    if os.path.exists(env.PATH_KEY):
        os.remove(env.PATH_KEY)
        os.remove(env.PATH_BACKUP)

    with pytest.raises(InvalidToken, match=re.escape('There was an error trying to decrypt the environment variables.')):
        env.decode_env()


# testa definir uma variável
def test_set_env(restart_system):
    # define uma variável de ambiente
    env.set_env(
        DB_USER = 'success'
    )

    assert env.DB_USER == 'success'


# testa tentar carregar as variáveis de ambiente sem que variáveis importantes existam
def test_load_file_env_value_error(restart_system):
    env.set_env(reload=False, DB_USER='None')
    
    with pytest.raises(ValueError, match=re.escape('Essential environment variables are missing. Redo the API configuration with "poetry run configure"')):
        env.load_file_env(True)

