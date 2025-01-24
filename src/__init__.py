import os
import time
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv, set_key


# retorna o logger de env
def env_logger():
    os.makedirs('./logs/', exist_ok=True)
    logger = logging.getLogger('env')

    if not logger.hasHandlers():
        handler = TimedRotatingFileHandler('./logs/env.log', when='midnight', interval=1, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


# salva .env com os dados padrões
def set_default_env(first: bool=False):
    if os.path.exists('.enc'):
        decode_env()

    with open('.env', 'w') as file:
        file.write('')

    set_env(
            reload=True,

            # dados do bot
            BOT_NAME='CryptoSentinel',
            ADM='paulindavzl',
            GITHUB='https://github.com/paulindavzl',
            LANG='pt',

            # define informações de conexão com banco de dados
            DB_USER='root',
            DB_PASSWORD='Null',
            DB_NAME='database',
            DB_HOST='localhost',
            DB_PORT=3306,

            # define informações de conexão com a Binance (indefinidas por padrão)
            ACCESS_KEY='Null',
            SECRET_KEY='Null',

            # define informações de configurações gerais
            DB_IS_CONFIGURED=False,
            API_IS_CONFIGURED=False,

            # define o tempo de troca de chaves
            TIME_CHANGE_KEY = 3600, # segundos (60 min)
            TIME_CHANGE_BACKUP_KEY = 600 # segundos (10 min)
        )

    # se é a primeira vez que estão sendo definidas, não tem problema
    if first:
        env_logger().info('Data in .env has been set to default')
    else: # se não é a primeira vez, pode ser um problema
        env_logger().warning('Data in .env has been set as default again')

    
# altera a chave
def change_key():
    if os.path.exists('.key'):
        os.remove('.key')
    
    get_key() # chama get_key somente para gerar uma nova chave
    env_logger().info('The key in .key has been changed')

    time.sleep(float(TIME_CHANGE_BACKUP_KEY)) # espera o tempo definido para trocar o backup da chave

    if os.path.exists('backup.key'):
        os.remove('backup.key')
    
    get_key(True)
    env_logger().info('The key in backup.key has been changed')


# obtém a chave de decodificação
def get_key(backup: bool=False, generate_backup: bool=True) -> str:
    key = ''
    prefix = 'backup' if backup else ''
    file_key = f'{prefix}.key'

    # garante que .key exista
    if not os.path.exists(file_key):
        if backup:
            if not os.path.exists('.key'):
                get_key(generate_backup=False)
            with open('.key', 'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()

        with open(file_key, 'wb') as file:
            file.write(key)
        
        if generate_backup and not backup:
            get_key(True)

        env_logger().info(f'The {prefix}.key file has been created') # carrega um log
    
    with open(file_key, 'rb') as file:
        key = file.read()
    
    return key


# codifica o arquivo .env
def encode_env():
    key = get_key() # obtém a chave
    content = ''

    if os.path.exists('.enc'):
        return

    if not os.path.exists('.env'):
        set_default_env()

    with open('.env', 'r') as file:
        content = file.read()

    # instancia a classe Fernet
    fernet = Fernet(key)
    content_encoded = fernet.encrypt(content.encode())

    # salva o arquivo criptografado
    with open('.enc', 'wb') as file:
        file.write(content_encoded)

    os.remove('.env') # apaga o conteúdo descriptografado


# decodifica o arquivo .enc
def decode_env():
    content = ''
    key = get_key()

    if os.path.exists('.env'):
        return 

    elif not os.path.exists('.enc'):
        set_default_env()

    with open('.enc', 'rb') as file:
        content = file.read()
        
    try:
        fernet = Fernet(key)
        content_decoded = fernet.decrypt(content)
    except InvalidToken:
        backup_key = get_key(True)
        try:
            fernet = Fernet(backup_key)
            content_decoded = fernet.decrypt(content)
        except InvalidToken:
            env_logger().critical(f'There was an error trying to decrypt the environment variables.')
            raise InvalidToken('There was an error trying to decrypt the environment variables.')

    # salva o arquivo descriptografado
    with open('.env', 'wb') as file:
        file.write(content_decoded)

    os.remove('.enc')


# define ou redefine o valor de uma variável de ambiente
def set_env(reload: bool=True, **envs):
    if os.path.exists('.enc'):
        decode_env()

    for key in envs:
        item = envs[key]
        if item == True:
            item = 'True'
        elif item == False:
            item = 'False'
        elif item == '':
            item = 'Null'

        set_key('.env', key, str(item))
        env_logger().info(f'The environment variable "{key}" has been assigned the value "{item}"')

    # recarrega as variáveis de ambiente
    if reload:
        load_file_env(True)

    encode_env()


# retorna uma variável específica
def get_env(env_name: str, digit: bool=False, alt=None, typ: type=int):
    env = os.getenv(env_name, alt)
    def isnumber() -> bool:
        try:
            float(env)
            return True
        except ValueError:
            return False

    if env == 'None':
        env = None
    elif env == 'True':
        env = True
    elif env == 'False':
        env = False
    elif digit and isnumber():
        env = typ(env)

    return env


# carrega as variáveis de ambiente
def load_file_env(reload: bool=False):
    global _initialized
    global BOT_NAME, ADM, GITHUB, LANG
    global DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT, DB_IS_CONFIGURED
    global ACCESS_KEY, SECRET_KEY, API_IS_CONFIGURED
    global TIME_CHANGE_KEY, TIME_CHANGE_BACKUP_KEY

    # caso _initialized não esteja definido
    if not '_initialized' in globals():
        _initialized = False

    # impede que .env fique sendo aberto, decodificado e codificado a todo momento
    if _initialized and not reload:
        return
        
    # garante que .env exista
    if not os.path.exists('.enc') and not os.path.exists('.env'):
        set_default_env(True if not reload and not _initialized else False)
    
    decode_env()
    load_dotenv(override=True)

    # dados do bot
    BOT_NAME = get_env('BOT_NAME', alt='CryptoSentinel')
    ADM = get_env('ADM', 'paulindavzl')
    GITHUB = get_env('GITHUB', 'https://github.com/paulindavzl')
    LANG = get_env('LANG', alt='pt')

    # dados para conexão com servidor MySQL
    DB_USER = get_env('DB_USER')
    DB_PASSWORD = get_env('DB_PASSWORD')
    DB_HOST = get_env('DB_HOST')
    DB_NAME = get_env('DB_NAME')
    DB_PORT = get_env('DB_PORT', digit=True, alt=3306, typ=int)

    # dados para conexão com Binance
    ACCESS_KEY = get_env('ACCESS_KEY')
    SECRET_KEY = get_env('SECRET_KEY')

    # tempo de troca de chave
    TIME_CHANGE_KEY = get_env('TIME_CHANGE_KEY', digit=True, alt=3600, typ=float)
    TIME_CHANGE_BACKUP_KEY = get_env('TIME_CHANGE_BACKUP_KEY', alt=600, digit=True, typ=float)

    # garante que existe as informações de conexão com o banco de dados
    db_variables = {'DB_HOST':DB_HOST, 'DB_NAME':DB_NAME, 'DB_PORT':DB_PORT, 'DB_USER':DB_USER, 'DB_PASSWORD':DB_PASSWORD}
    if not all([DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER]):
        missing = []
        for i in db_variables:
            if db_variables[i] is None:
                missing.append(i)
        set_env(False, DB_IS_CONFIGURED=False) # para facilitar a configuração
        env_logger().critical(f'Missing essential environment variables: {missing}')
        raise ValueError('Essential environment variables are missing. Redo the API configuration with "poetry run configure"')

    # garante que existe as chaves de API para conexão com Binance
    api_variables = {'ACESS_KEY': ACCESS_KEY, 'SECRET_KEY': SECRET_KEY}
    if not all([ACCESS_KEY, SECRET_KEY]):
        missing = []
        for i in api_variables:
            if api_variables[i] is None:
                missing.append(i)
        set_env(API_IS_CONFIGURED=False, reload=False) # para facilitar a configuração
        env_logger().critical(f'Missing essential environment variables: {missing}')
        raise ValueError('Essential environment variables are missing. Redo the API configuration with "poetry run configure"')

    # dados de configurações gerais
    DB_IS_CONFIGURED = get_env('DB_IS_CONFIGURED')
    API_IS_CONFIGURED = get_env('API_IS_CONFIGURED')

    _initialized = True
    encode_env()
    env_logger().info('Environment variables have been loaded')
    

# realiza a leitura inicial de .env
try:
    load_file_env()
except Exception as e:
    env_logger().critical(f'A critical error has occurred:\n{traceback.format_exc()}')
    raise e
