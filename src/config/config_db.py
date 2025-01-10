from types import FunctionType
from src import  DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from src.config import config_logger
from src.core.utis import hide_data, clear, gen_input, exec_command


# inicia a configuração do banco de dados
def start(commands) -> dict | None:
    config_db = f'''{'-'*30}
Você está realizando a configuração do seu banco de dados MySQL. (Use [/pass] para passar, [/restart] para reiniciar, [/cancel] para cancelar configuração)
{'-'*30}
'''

    index = 0
    items = [['Informe o usuário (user)', DB_USER, False], ['Informe a senha (password)', DB_PASSWORD, True], ['Informe o servidor (host)', DB_HOST, False], ['Informe o nome do banco de dados (database)', DB_NAME, False], ['Informe a porta (port)', DB_PORT, False]]

    for item in items:
        clear(config_db)
        response = gen_input(item[0], item[1], commands, 'Database', start, item[2])
        if response is None:
            return
        elif isinstance(response, FunctionType):
            return start(commands)
        
        match index:
            case 0: db_user = response
            case 1: db_password = response
            case 2: db_host = response 
            case 3: db_name = response
            case 4: db_port = response

        index += 1

    return end_config(commands, db_user=db_user, db_host=db_host, db_name=db_name, db_password=db_password, db_port=db_port)


def end_config(commands, **db) -> dict | None:
    db_user = db.get('db_user')
    db_password = db.get('db_password')
    db_host = db.get('db_host')
    db_name = db.get('db_name')
    db_port = db.get('db_port')

    response = input(f'''Você concluiu a configuração do banco de dados MySQL com os seguintes dados:
user: {db_user}
password: {hide_data(db_password)}
host: {db_host}
database: {db_name}
port: {db_port}

Aperte ENTER para continuar ou digite: [/cancel] para cancelar, [/restart] para reiniciar\n>> 
''')

    if response == '/restart':
        config_logger().info('Once completed, the database configuration was restarted')
        return start(commands)
    
    elif response == '/cancel':
        config_logger().info('Once completed, the database configuration was canceled')
        return

    config_logger().info('Database configuration is complete')
    return {'user': db_user, 'password': db_password, 'host': db_host, 'name': db_name, 'port': db_port}