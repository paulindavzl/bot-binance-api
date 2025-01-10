import os
from src import DB_IS_CONFIGURED, API_IS_CONFIGURED
from src.config import config_logger
from src.config import config_api, config_db
from src.core.utis import hide_data, clear, exec_command
    

# inicia a configuração
def start():
    config_logger().info('Configuration has started')
    commands = ['/pass', '/restart', '/cancel']
    
    clear()

    if DB_IS_CONFIGURED:
        response = input('O banco de dados já foi configurado. Deseja realizar a configuração novamente? [ENTER] para continuar | [/pass ou /cancel] para cancelar reconfiguração\n>>')
        if not response in commands:
            config_logger().warning('Database configuration has started again.')
            data_db = config_db.start(commands)
    else:
        config_logger().info('Database configuration has started')
        data_db = config_db.start(commands)

    

    if API_IS_CONFIGURED:
        response = input('Os dados da API já foram configurados. Deseja realizar a configuração novamente? [ENTER] para continuar | [/pass ou /cancel] para cancelar reconfiguração\n>>')
        if not response in commands:
            config_logger().warning('API configuration has started again.')

    else:
        config_logger().info('API configuration has started')

