import os
import logging
from src.core.lang import c, path, langs
from src.core.utils import wait, clear
from src.config import config_logger

def run(envlib, autoconfirm: bool=False, autoden: bool=False, test: bool=False):
    logs = 'logs'
    enc = 'data/.enc'
    env = 'data/.env'
    key = 'data/.key'
    backup = 'data/backup.key'

    restart_pass = 'RESTART SYSTEM'
    config_logger().warning(f'System Restore has started.\nPass: {restart_pass}\nAutoconfirm: {str(autoconfirm)}\nAutodeny: {autoden}')
    response = restart_pass
    if not autoconfirm:
        clear(f'{c(langs(envlib)[envlib.LANG]['RESTART_SYSTEM_CONFIRM'], 'r')}\n{c('Digite:' if envlib.LANG == 'pt' else 'Type:', 'r', 'w')} {restart_pass}')
        response = input(f'{path(envlib)} ')
    if response == restart_pass and not autoden:
        logging.shutdown()

        # apaga todos os logs
        if os.path.exists(logs):
            logs_list = os.listdir(logs)
            for log in logs_list:
                if log != 'system.log':
                    os.remove(os.path.join(logs, log))
            
        # apaga .key 
        if os.path.exists(key):
            os.remove(key)
        
        # apaga .enc 
        if os.path.exists(enc):
            os.remove(enc)

        # apaga .env
        if os.path.exists(env):
            os.remove(env)

        # apaga backup.key
        if os.path.exists(backup):
            os.remove(backup)

        config_logger().warning('The system has been restarted')
        clear(c(langs(envlib)[envlib.LANG]['RESTART_SYSTEM_SUCCESSFULLY'], 'g'))
        wait(envlib, langs)
        envlib._initialized = False
        envlib.load_file_env()
        return
    
    config_logger().info('Restore canceled')
    clear(c('Restauração cancelada!' if envlib.LANG == 'pt' else 'Restore canceled!', 'g'))
    wait(envlib, langs)