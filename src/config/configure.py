import os
import traceback
import src.__init__ as env
from src.config import config_logger
from src.config.err import show_error
from src.config.parser import Parser, ParserError
from src.core.lang import c, path, langs, clear
from src.core.utils import wait
from src.config.execute_comands import Execute


def default_panel():
    msg = langs(env)[env.LANG]['MSG_DEFAULT_PANEL']
    return c(msg, 'y')


# inicia a configuração banco de dados
def start():
    try:
        config_logger().info('Configuration has started')
        db_configuration_level = 0
        api_configuration_level = 0

        while True:
            clear(default_panel() + '\033[0m')
            response = input(f'{path(env)} ')

            # mostra os comando com exemplo de uso
            if '--help' in response: 
                clear(f'{path(env)} {response}\n\n{c(langs(env)[env.LANG]['HELP_COMMANDS'], 'y')}')
                wait(env, langs)

            # finaiza a configuração
            elif 'exit' in response: 
                clear()
                config_logger().info('The configuration is finished')
                exit()
            
            # analiza e executa os comando
            else:
                parser = Parser(response).result
                err = parser.get('err')
                if err:
                    err_message = show_error(err, env)

                    config_logger().error(f'''There was an error parsing the commands.
Error name: {err.name}
Item: {err.item}
Type: {err.typ}
Message: {err_message}
Command line: {response}''')

                    clear(f'{path(env)} {response}\n{c(err_message, 'r')}')
                    wait(env, langs)

                else:
                    execute = Execute(parser, env, response)
                    make_logs(execute, response)
    except Exception as e:
        config_logger().critical(f'A critical error has occurred:\n{traceback.format_exc()}')
        raise e


# gera os logs pós execução
def make_logs(execute, response: str):
    commands = execute.executed

    if '--restart_system' in commands:
        config_logger().info('Configuration has started')

    if commands:
        config_logger().info(f'Command line: {response}')
        for cmd in commands:
            config_logger().info(f'Command executed successfully: {cmd}')