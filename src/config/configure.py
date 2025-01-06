import os
import json
from src import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, DB_IS_CONFIGURED, API_IS_CONFIGURED


# limpa o terminal
def clear(info:[str]=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    if info:
        print(info)


# esconde a senha
def hide_password(password) -> str:
    if len(password) >= 4:
        n_pass = password[0]+'*'*(len(password)-2)+password[-1]
    elif len(password) > 0:
        n_pass = '*'*len(password)
    else:
        n_pass = password
    
    return n_pass


# inicia a configuração do banco de dados
def start_config_db(commands):
    config_db = f'''{'-'*30}
Você está realizando a configuração do seu banco de dados MySQL. ([/pass] para passar, [/restart] para reiniciar, [/cancel] para cancelar configuração)
{'-'*30}
'''
    clear(config_db)

    # obtém o user
    response = input(f'Informe o usuário (user). Atual: {DB_USER}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_USER
        else:
            return exec_command(response, start_config_db, commands)

    db_user = response
    clear(config_db)

    # obtém o password
    response = input(f'Informe a senha (password). Atual: {hide_password(DB_PASSWORD)}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_PASSWORD
        else:
            return exec_command(response, start_config_db, commands)

    db_password = response
    clear(config_db)

    # otém o host
    response = input(f'Informe o servidor (host). Atual: {DB_HOST}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_HOST
        else:
            return exec_command(response, start_config_db, commands)

    db_host = response
    clear(config_db)

    # otém o banco de dados
    response = input(f'Informe o nome do banco de dados (database). Atual: {DB_NAME}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_NAME
        else:
            return exec_command(response, start_config_db, commands)

    db_name = response
    clear(config_db)

    # otém a port
    response = input(f'Informe a porta (port). Atual: {DB_PORT}\n>> ')
    
    if response in commands:
        if response == '/pass':
            response = DB_PORT
        else:
            return exec_command(response, start_config_db, commands)

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
def exec_command(command, funct, commands):
    if command == '/restart':
        return funct(commands)
    

# inicia a configuração
def start():
    commands = ['/pass', '/restart', '/cancel']
    
    if DB_IS_CONFIGURED:
        response = input('O banco de dados já foi configurado. Deseja realizar a configuração novamente? [ENTER] para continuar | [/pass ou /cancel] para cancelar reconfiguração\n>>')
        if response in commands:
            config_db = start_config_db(commands)
    else:
        config_db = start_config_db(commands)



