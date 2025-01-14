from types import FunctionType
from src import  ACCESS_KEY, SECRET_KEY
from src.config import config_logger
from src.core.utils import hide_data, clear, gen_input


# inicia a configuração da API
def start(commands) -> dict | None:
    config_db = f'''{'-'*30}
Você está realizando a configuração da sua API Binance. (Use [/pass] para passar, [/restart] para reiniciar, [/cancel] para cancelar configuração)
{'-'*30}
'''

    index = 0
    items = [['Informe a chave de acesso (Access Key)', ACCESS_KEY, True], ['Informe a chave secreta (Secret Key)', SECRET_KEY, True]]

    for item in items:
        clear(config_db)
        response = gen_input(item[0], item[1], commands, 'API', start, item[2])
        if response is None:
            return
        elif isinstance(response, FunctionType):
            return start(commands)
        
        match index:
            case 0: access_key = response
            case 1: secret_key = response

        index += 1

    return end_config(commands, access_key=access_key, secret_key=secret_key)


def end_config(commands, **api) -> dict | None:
    access_key = api.get('access_key')
    secret_key = api.get('secret_key')

    response = input(f'''Você concluiu a configuração da API Binance com os seguintes dados:
Access Key: {hide_data(access_key)}
Secret Key: {hide_data(secret_key)}

Aperte ENTER para continuar ou digite: [/cancel] para cancelar, [/restart] para reiniciar\n>> 
''')

    if response == '/restart':
        config_logger().info('Once completed, the API configuration was restarted')
        return start(commands)
    
    elif response == '/cancel':
        config_logger().info('Once completed, the API configuration was canceled')
        return

    config_logger().info('API configuration is complete')
    return {'access_key': access_key, 'secret_key': secret_key}