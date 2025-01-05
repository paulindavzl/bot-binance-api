import os
import json
from src import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from src.config import PATH_CONFIG, DEFAULT_CONFIG_JSON


# carrega o arquivo de configuração
def load_config_json() -> dict:
    json_path = f'{PATH_CONFIG}/config.json'

    # garante que config.json exista
    if not os.path.exists(json_path):
        with open(json_path, 'w') as file:
            file.write(DEFAULT_CONFIG_JSON)

    # carrega as configurações
    json_config = {'is_configured': 0}
    with open(json_path, 'r') as file:
        try:
            json_config = json.load(file)
        except json.JSONDecodeError as e:
            print(f'Houve um erro ao abrir o arquivo de confuração: {e}')
        except Exception as e:
            print(f'Houve um erro desconhecido: {e}')

    return json_config


# limpa o terminal
def clear(info:[str]=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    if info:
        print(info)


# esconde a senha
def hide_password(password) -> str:
    n_pass = password[0]+'*'*(len(password)-2)+password[-1]
    
    return n_pass


# inicia a configuração do banco de dados
def start_config_db(status, commands):
    config_db = f'''{'-'*30}
Você está realizando a configuração do seu banco de dados MySQL. ([/pass] para passar, [/restart] para reiniciar, [/cancel] para cancelar configuração)
{'Obs: as configurações já foram feitas antes!' if status == 0 else ''}
{'-'*30}
'''

    # obtém o user
    response = input(f'Informe o usuário (user). Atual: {DB_USER}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_USER
        else:
            return exec_command(response, start_config_db, status, commands)

    db_user = response
    clear(config_db)

    # obtém o password
    response = input(f'Informe a senha (password). Atual: {hide_password(DB_PASSWORD)}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_PASSWORD
        else:
            return exec_command(response, start_config_db, status, commands)

    db_password = response
    clear(config_db)

    # otém o host
    response = input(f'Informe o servidor (host). Atual: {DB_HOST}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_HOST
        else:
            return exec_command(response, start_config_db, status, commands)

    db_host = response
    clear(config_db)

    # otém o banco de dados
    response = input(f'Informe o nome do banco de dados (database). Atual: {DB_NAME}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_NAME
        else:
            return exec_command(response, start_config_db, status, commands)

    db_name = response
    clear(config_db)

    # otém a port
    response = input(f'Informe a porta (port). Atual: {DB_PORT}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_PORT
        else:
            return exec_command(response, start_config_db, status, commands)

    db_port = response
    clear()

    response = input(f'''Você concluiu a configuração do banco de dados MySQL com os seguintes dados:
user: {db_user}
password: {hide_password(db_password)}
host: {db_host}
database: {db_name}
port: {db_port}

Aperte ENTER para continuar ou digite: [/cancel] para cancelar, [/restart] para reiniciar\n>> 
''')

    if response == '/restart':
        return start_config_db()
    
    elif response == '/cancel':
        return

    return db_user,db_password, db_host, db_name, db_port

    
# executa o comando que o usuário selecionou
def exec_command(command, funct, status, commands):
    if command == '/restart':
        return funct(status, commands)
    

# inicia a configuração
def start():
    config = load_config_json()
    status = config.get('is_configured')
    commands = ['/pass', '/restart', '/cancel']
    
    config_db = start_config_db(status, commands)



