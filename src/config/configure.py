import os
from src import DB_IS_CONFIGURED, API_IS_CONFIGURED,  DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, ACCESS_KEY, SECRET_KEY, set_env
from src.config import config_logger
from src.config import config_api, config_db
from src.core.utils import hide_data, clear, exec_command
from src.modals import is_connected


# introdução à configuração do banco de dados
def intro_config_db(commands, msg: str=None):
    clear(msg)
    if DB_IS_CONFIGURED:
        response = input('O banco de dados já foi configurado. Deseja realizar a configuração novamente? [ENTER] para continuar | [/pass ou /cancel] para cancelar reconfiguração\n>>')
        if not response in commands:
            config_logger().warning('Database configuration has started again.')
            return config_db.start(commands)
        else:
            return response
            
    else:
        config_logger().info('Database configuration has started')
        return config_db.start(commands)


# introdução à configuração da API
def intro_config_api(commands, msg: str=None):
    clear(msg)
    if API_IS_CONFIGURED:
        response = input('Os dados da API já foram configurados. Deseja realizar a configuração novamente? [ENTER] para continuar | [/pass ou /cancel] para cancelar reconfiguração\n>>')
        if not response in commands:
            config_logger().warning('API configuration has started again.')
            return config_api.start(commands)
        else:
            return response

    else:
        config_logger().info('API configuration has started')
        return config_api.start(commands)
    

# inicia a configuração
def start():
    config_logger().info('Configuration has started')
    commands = ['/pass', '/restart', '/cancel']

    continue_config_db = True
    data_db = intro_config_db(commands) # inicia a configuração o banco de dados
    while continue_config_db:
        print(data_db)
        input('')
        match data_db:
            case '/pass': continue_config_db = False # cancela a verificação
            case '/cancel':
                continue_config_db = False # cancela a verificação
                config_logger().info('Configuration has been canceled')
                continue_config_db = False # cancela a verificação
                return
            case _:
                # caso a resposta do usuário não for um comando
                if data_db is None: # verifica se é None 
                    data_db = {
                        'user': DB_USER,
                        'host': DB_HOST,
                        'password': DB_PASSWORD,
                        'port': DB_PORT,
                        'name': DB_NAME
                    }
                
                # executa as mudanças feitas pelo usuário
                set_env(
                    DB_USER=data_db.get('user'),
                    DB_HOST=data_db.get('host'),
                    DB_PASSWORD=data_db.get('password'),
                    DB_PORT=data_db.get('port'),
                    DB_NAME=data_db.get('name')
                )

                # testa se é possível estabelecer uma conexão com o banco de dados
                if not is_connected(): # se não for possível informa ao usuário e refaz o processo
                    config_logger().error('Unable to connect to the database using the data provided')
                    data_db = intro_config_db(commands, msg='Unable to connect to the database using the data provided. Try again.')
                else:
                    continue_config_db = False # cancela a verificação
                    set_env(DB_IS_CONFIGURED=1)

    continue_config_api = True
    data_api = intro_config_api(commands)
    while continue_config_api:
        match data_api:
            case '/pass': continue_config_api = False # cancela a verificação
            case '/cancel':
                continue_config_api = False # cancela a verificação
                config_logger().info('Configuration has been canceled')
                return
            case _:
                # caso a resposta do usuário não for um comando
                if data_api is None: # verifica se é None 
                    data_api = {
                        'api_key': API_KEY,
                        'secret_key': SECRET_KEY
                    }
                
                # executa as mudanças feitas pelo usuário
                set_env(
                    API_KEY=data_api.get('api_key'),
                    SECRET_KEY=data_api.get('secret_key'),
                )

                # testa se é possível estabelecer uma conexão com a API
                if not is_connected('api'): # se não for possível informa ao usuário e refaz o processo
                    config_logger().error('Unable to connect to the Binance using the data provided')
                    data_db = intro_config_db(commands, msg='Unable to connect to the Binance using the data provided. Try again.')
                else:
                    continue_config_api = False # cancela a verificação
                    set_env(API_IS_CONFIGURED=1)

    config_logger().info('The configuration was completed successfully')
    input('Configuração finalizada com sucesso! Aperte ENTER para fechar.')
    exit()
