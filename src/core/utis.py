import os
from src.config import config_logger

# esconde um dado
def hide_data(data: str) -> str:
    if len(str(data)) >= 4:
        hide = str(data)[0]+'*'*(len(str(data))-2)+str(data)[-1]
    elif len(str(data)) > 0:
        hide = '*'*len(str(data))
    else:
        hide = str(data)
    
    return hide


# limpa o terminal
def clear(info:[str]=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    if info:
        print(info)

    
# gera o input e analisa
def gen_input(msg: str, data, commands: list, config: str, funct, hide: bool=False):
    response = input(f'{msg}. Atual: {hide_data(data) if hide else data}\n>> ')
    if response in commands:
        if response == '/pass':
            response = data
            return response
        return exec_command(response, funct, name=config)
    
    return response


# executa o comando que o usuário selecionou
def exec_command(command, funct, name):
    if command == '/restart':
        config_logger().info(f'{name} configuration has been reset')
        return funct
    config_logger().info(f'{name} configuration has been canceled')
    return 

