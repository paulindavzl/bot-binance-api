import os
import traceback
import src.__init__ as env
from src.config import config_logger
from src.config.err import show_error
from src.config.parser import Parser, ParserError
from src.core.lang import c, path, langs, clear
from src.core.utils import wait
from src.core.emails import manager as email
from src.config.execute_comands import Execute


def default_panel():
    msg = langs(env)[env.LANG]['MSG_DEFAULT_PANEL']
    return c(msg, 'y')
    
# inicia a configuração banco de dados
def start():
    try:
        config_logger().info('Configuration has started')
        db_items = {'--user': False, '--host': False, '--port': False, '--pass': False, '--dbname': False}
        api_items = {'--accesskey': False, '--secretkey': False}
        email_items = {'--emailaddress': False, '--emailpass': False}

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

                    config_logger().error(f'There was an error parsing the commands.\n\tError name: {err.name}\n\tItem: {err.item}\n\tType: {err.typ}\n\tMessage: {err_message}\n\tCommand line: {response}')

                    clear(f'{path(env)} {response}\n{c(err_message, 'r')}')
                    wait(env, langs)

                else:
                    execute = Execute(parser, env, response)

                    if execute.executed:
                        for cmd in execute.executed:
                            if cmd in db_items:
                                db_items[cmd] = True
                            elif cmd in api_items:
                                api_items[cmd] = True
                            elif cmd in email_items:
                                email_items[cmd] = True

                    make_logs(execute, response)

                    if all_true(db_items): env.set_env(DB_IS_CONFIGURED=True)
                    if all_true(api_items): env.set_env(API_IS_CONFIGURED=True)
                    if all_true(email_items): email.SendEmail(env, to=env.EMAIL_ADDRESS, subject='email_test', content='email_test'); wait(env, langs)

    except Exception as e:
        config_logger().critical(f'A critical error has occurred:\n{traceback.format_exc()}')
        raise e


# gera os logs pós execução
def make_logs(execute, response: str):
    commands = execute.executed

    if commands:
        if '--restart_system' in commands:
            config_logger().info('Configuration has started')
            
        for cmd in commands:
            config_logger().info(f'Command executed successfully: {cmd}')


# verifica se todos os valores são True
def all_true(data: dict) -> bool:
    for value in data.values():
        if not value: return False
    
    return True