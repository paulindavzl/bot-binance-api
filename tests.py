import pytest
import traceback
from src.system_logger import sys_logger
from src.core.lang import c

'''
facilita a execução dos testes pelo Poetry
a partir do ambiente do Poetry (poetry shell) execute: poetry run tests
contêiner Docker, execute: docker-compose run tests
'''

def run():
    try:
        sys_logger().info('Tests are being initialized')
        print(c('Be aware that running tests outside of a Docker container will delete all important information and leave it at default.', 'r', 'w'))
        response = input(f'Type [ {c('y', 'g', 'w')} ] to continue: ')
        if response == 'y':
            sys_logger().warning('Tests have been initialized')
            pytest.main(['tests/', '-vv'])
        else:
            sys_logger().info('Tests were canceled')
            print(c('Canceled', 'r', 'w'))
    except Exception as e:
        sys_logger().critical(f'A critical error has occurred:\n{traceback.format_exc()}')
        raise e