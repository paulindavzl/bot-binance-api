import os
import pytest
import logging
from unittest.mock import patch
from src import DB_HOST, DB_IS_CONFIGURED, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, API_IS_CONFIGURED
from src.config import configure, config_api, config_db


# apaga todos os logs, .key, .enc e .env (não executar teste fora do contêiner Docker de testes [docker-compose testes])
@pytest.fixture
def restart_system():
    logs = './logs'
    enc = './.enc'
    env = './.env'
    key = './.key'

    def remove_all():
        logging.shutdown()

        # apaga todos os logs
        if os.path.exists(logs):
            logs_list = os.listdir(logs)
            for log in logs_list:
                if log != 'test.log':
                    os.remove(f'{logs}/{log}')
        
        # apaga .key 
        if os.path.exists(key):
            os.remove(key)
        
        # apaga .enc 
        if os.path.exists(enc):
            os.remove(enc)

        # apaga .env 
        if os.path.exists(env):
            os.remove(env)
        
    remove_all()

    yield

    remove_all()


# comandos
@pytest.fixture
def commands():
    command_list = ['/pass', '/restart', '/cancel']
    return command_list


# obtém os dados em config.log
def get_config(method: str='read'):
    config = ''
    with open('./logs/config.log', 'r') as log:
        if method == 'readlines':
            config = log.readlines()
        else:
            config = log.read()

    return config


# retorna os dados para config_db
@pytest.fixture
def data_config_db():
    data = ['test_user', 'test123', '/pass', 'test_db', 8080, '']
    return data


# testa configurar o banco de dados
def test_config_db(restart_system, commands, data_config_db):
    response = ''
    with patch('builtins.input', side_effect=data_config_db):
        response = config_db.start(commands)

    # confirma user
    assert response.get('user') != DB_USER and response.get('user') == data_config_db[0]

    # confirma password
    assert response.get('password') != DB_PASSWORD and response.get('password') == data_config_db[1]

    # confirma host
    assert response.get('host') == DB_HOST

    # confirma database
    assert response.get('name') != DB_NAME and response.get('name') == data_config_db[3]

    #confirma port
    assert response.get('port') != DB_PORT and response.get('port') == data_config_db[4]

    # confirma config.log 
    assert get_config()[23:-1] == ' - INFO - Database configuration is complete'


# testa reiniciar a configuração bem no início
def test_config_db_init_restart(restart_system, commands, data_config_db):
    new_data = ['/restart']
    new_data.extend(data_config_db)

    with patch('builtins.input', side_effect=new_data):
        response = config_db.start(commands)
    
    # confirma em config.log
    assert get_config('readlines')[0][23:-1] == ' - INFO - Database configuration has been reset'

    
# testa reiniciar a configuração no final
def test_config_db_end_restart(restart_system, commands, data_config_db):
    new_data = data_config_db[:-1]
    new_data.extend(['/restart'])
    new_data.extend(data_config_db)

    with patch('builtins.input', side_effect=new_data):
        response = config_db.start(commands)
    
    # confirma em config.log
    assert get_config('readlines')[0][23:-1] == ' - INFO - Once completed, the database configuration was restarted'


# testa cancelar a configuração bem no início
def test_config_db_init_cancel(restart_system, commands, data_config_db):
    with patch('builtins.input', return_value='/cancel'):
        response = config_db.start(commands)
    
    # confirma em config.log
    assert get_config('readlines')[0][23:-1] == ' - INFO - Database configuration has been canceled'


# testa cancelar a configuração no final
def test_config_db_end_cancel(restart_system, commands, data_config_db):
    new_data = data_config_db[:-1]
    new_data.extend(['/cancel'])
    
    with patch('builtins.input', side_effect=new_data):
        response = config_db.start(commands)
    
    # confirma em config.log
    assert get_config('readlines')[0][23:-1] == ' - INFO - Once completed, the database configuration was canceled'