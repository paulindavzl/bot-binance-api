import os
import pytest
import logging
from src import *


# apaga todos os logs, .key (backup.key), .enc e .env (não executar teste fora do contêiner Docker de testes [docker-compose testes])
@pytest.fixture
def restart_system():
    logs = './logs'
    delete_this = ['./.enc', './.env', './.key', './backup.key']

    def remove_all():
        logging.shutdown()

        # apaga todos os logs
        if os.path.exists(logs):
            logs_list = os.listdir(logs)
            for log in logs_list:
                os.remove(f'{logs}/{log}')
        
        for item in delete_this:
            if os.path.exists(item):
                os.remove(item)
        
        
    remove_all()

    yield

    remove_all()


# testa alterar o tempo de troca de chaves
def test_set_time_change_key(restart_system):
    set_time_change_key(50, 5, True)

    assert int(TIME_CHANGE_KEY) == (50 * 60)
    assert TIME_CHANGE_BACKUP_KEY == 5 * 60


def test_set_env(restart_system):
    set_env(
        TEST_VARIABLE = 'success'
    )

    decode_env()

    assert os.getenv('TEST_VARIABLE') == 'success'
