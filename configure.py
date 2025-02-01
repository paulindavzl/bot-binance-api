import traceback
import src.__init__ as env
from src.system_logger import sys_logger
from src.config import configure


'''
facilita a execução das configurações
no ambiente do Poetry (poetry shell), execute: poetry run configure
'''

def run():
    try: 
        sys_logger().info('Configuration started')
        sys_logger().info(f'Database: {'configured' if env.DB_IS_CONFIGURED else 'not configured'} / API: {'configured' if env.API_IS_CONFIGURED else 'not configured'}')
        configure.start()
    except Exception as e:
        sys_logger().critical(f'A critical error has occurred:\n{traceback.format_exc()}')
        raise e