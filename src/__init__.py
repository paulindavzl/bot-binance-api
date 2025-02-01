import os
import time
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv, set_key
import src.key_mechanism as km


PATH_LOGS = './logs'
PATH_ENV = './data/.env'
PATH_ENC = './data/.enc'
PATH_KEY = './data/.key'
PATH_BACKUP = './data/backup.key'

class Envlib:

    def __init__(self):
        self.PATH_KEY = PATH_KEY
        self.PATH_BACKUP = PATH_BACKUP
        self.env_logger = env_logger

# retorna o logger de env
def env_logger():
    os.makedirs(PATH_LOGS, exist_ok=True)
    logger = logging.getLogger('env')

    if not logger.hasHandlers():
        handler = TimedRotatingFileHandler(f'{PATH_LOGS}/env.log', when='midnight', interval=1, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


# salva .env com os dados padrões
def set_default_env(first: bool=False):
    if os.path.exists(PATH_ENC):
        decode_env()

    with open(PATH_ENV, 'w') as file:
        file.write('')

    set_env(
            reload=True,

            # dados do bot
            BOT_NAME='CryptoSentinel',
            ADM='paulindavzl',
            GITHUB='https://github.com/paulindavzl',
            LANG='pt',
            DEBUG=True,

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


# codifica o arquivo .env
def encode_env():
    key = km.get_key(env=Envlib()) # obtém a chave
    content = ''

    if os.path.exists(PATH_ENC):
        return

    if not os.path.exists(PATH_ENV):
        set_default_env()

    with open(PATH_ENV, 'r') as file:
        content = file.read()

    # instancia a classe Fernet
    fernet = Fernet(key)
    content_encoded = fernet.encrypt(content.encode())

    # salva o arquivo criptografado
    with open(PATH_ENC, 'wb') as file:
        file.write(content_encoded)

    os.remove(PATH_ENV) # apaga o conteúdo descriptografado


# decodifica o arquivo .enc
def decode_env():
    content = ''
    key = km.get_key(env=Envlib())

    if os.path.exists(PATH_ENV):
        return 

    elif not os.path.exists(PATH_ENC):
        set_default_env()

    with open(PATH_ENC, 'rb') as file:
        content = file.read()
        
    try:
        fernet = Fernet(key)
        content_decoded = fernet.decrypt(content)
    except InvalidToken:
        backup_key = km.get_key(True, env=Envlib())
        try:
            fernet = Fernet(backup_key)
            content_decoded = fernet.decrypt(content)
        except InvalidToken:
            env_logger().critical(f'There was an error trying to decrypt the environment variables.')
            raise InvalidToken('There was an error trying to decrypt the environment variables.')

    # salva o arquivo descriptografado
    with open(PATH_ENV, 'wb') as file:
        file.write(content_decoded)

    os.remove(PATH_ENC)


# define ou redefine o valor de uma variável de ambiente
def set_env(reload: bool=True, **envs):
    if os.path.exists(PATH_ENC):
        decode_env()

    for key in envs:
        item = envs[key]
        if item == True:
            item = 'True'
        elif item == False:
            item = 'False'
        elif item == '':
            item = 'Null'

        set_key(PATH_ENV, key, str(item))
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
        except Exception as e:
            if isinstance(e, (ValueError, TypeError)):
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
    global BOT_NAME, ADM, GITHUB, LANG, DEBUG
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
    if not os.path.exists(PATH_ENC) and not os.path.exists(PATH_ENV):
        set_default_env(True if not reload and not _initialized else False)
    
    decode_env()
    load_dotenv(PATH_ENV, override=True)

    # dados do bot
    BOT_NAME = get_env('BOT_NAME', alt='CryptoSentinel')
    ADM = get_env('ADM', 'paulindavzl')
    GITHUB = get_env('GITHUB', 'https://github.com/paulindavzl')
    LANG = get_env('LANG', alt='pt')
    DEBUG = get_env('DEBUG', alt=True)

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
    if not os.path.exists('./data'): os.makedirs('./data', exist_ok=True)
    load_file_env()
except Exception as e:
    env_logger().critical(f'A critical error has occurred:\n{traceback.format_exc()}')
    raise e
