import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key


TIME_CHANGE_KEY = 30 # em minutos
TIME_CHANGE_BACKUP_KEY = 10 # em minutos


# retorna o logger para salvar logs
import logging

# retorna o logger de core
def env_logger():
    global _logger_initialized

    if not '_logger_initialized' in globals():
        _logger_initialized = False
    
    os.makedirs('./logs/', exist_ok=True)
    logger = logging.getLogger('env')

    if not _logger_initialized:
        handler = TimedRotatingFileHandler('./logs/env.log', when='midnight', interval=7, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        _logger_initialized = True

    return logger



# salva .env com os dados padrões
def set_default_env(first: bool=False):
    set_env(
            # define informações de conexão com banco de dados
            DB_USER='root',
            DB_PASSWORD='NULL',
            DB_NAME='database',
            DB_HOST='localhost',
            DB_PORT=3306,

            # define informações de conexão com a Binance (indefinidas por padrão)
            API_KEY='NULL',
            SECRET_KEY='NULL',

            # define informações de configurações gerais
            TEST_MODE=0,
            DB_IS_CONFIGURED=0,
            API_IS_CONFIGURED=0
        )

    # se é a primeira vez que estão sendo definidas, não tem problema
    if first:
        env_logger().info('Data in .env has been set to default')
    else: # se não é a primeira vez, pode ser um problema
        env_logger().warning('Data in .env has been set to default')

    
# altera a chave
def change_key():
    if os.path.exists('.key'):
        os.remove('.key')
    
    get_key() # chama get_key somente para gerar uma nova chave
    env_logger().info('The key in .key has been changed')

    time.sleep(TIME_CHANGE_BACKUP_KEY)

    if os.path.exists('backup.key'):
        os.remove('backup.key')
    
    get_key(True)
    env_logger().info('The key in backup.key has been changed')


# obtém a chave de decodificação
def get_key(backup: bool=False) -> str:
    key = ''
    prefix = 'backup' if backup else ''
    file_key = f'{prefix}.key'

    # garante que .key exista
    if not os.path.exists(file_key):
        key = Fernet.generate_key()
        with open(file_key, 'wb') as file:
            file.write(key)

        env_logger().info(f'The {prefix}.key file has been created') # carrega um log
    
    with open(file_key, 'rb') as file:
        key = file.read()
    
    return key


# codifica o arquivo .env
def encode_env():
    key = get_key() # obtém a chave
    content = ''

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

    if not os.path.exists('.enc'):
        fernet = Fernet(key)
        content_encoded = fernet.encrypt(content.encode())
        with open('.enc', 'wb') as file:
            file.write(content_encoded)

    with open('.enc', 'rb') as file:
        content = file.read()
        
    try:
        fernet = Fernet(key)
        content_decoded = fernet.decrypt(content)
    except InvalidToken:
        backup_key = get_key(True)
        try:
            fernet = Fernet(key)
            content_decoded = fernet.decrypt(content)
        except InvalidToken:
            manager

    # salva o arquivo descriptografado
    with open('.env', 'wb') as file:
        file.write(content_decoded)

    os.remove('.enc')


# define ou redefine o valor de uma variável de ambiente
def set_env(**envs):
    if os.path.exists('.enc'):
        decode_env()

    for key in envs:
        set_key('.env', key, str(envs[key]))
        env_logger().info(f'The environment variable {key} has been assigned the value {envs[key]}')

    encode_env()


# carrega as variáveis de ambiente
def load_file_env(reload: bool=False):
    global _initialized
    global DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
    global API_KEY, SECRET_KEY, TEST_MODE, DB_IS_CONFIGURED, API_IS_CONFIGURED

    # caso _initialized não esteja definido
    if not '_initialized' in globals():
        _initialized = False

    # impede que .env fique sendo aberto, decodificado e codificado a todo momento
    if _initialized and not reload:
        return
        
    # garante que .env exista
    if not os.path.exists('.env') and not os.path.exists('.enc'):
        set_default_env(True)
    

    decode_env()
    load_dotenv()


    # dados para conexão com servidor MySQL
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = int(os.getenv('DB_PORT', 3306))

    # dados para conexão com Binance
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # garante que existe as informações de conexão com o banco de dados
    if not all([DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD]):
        set_env(DB_IS_CONFIGURED=0) # para facilitar a configuração
        env_logger().critical(f'Missing essential environment variables')
        raise ValueError('Faltam variáveis de ambiente essenciais. Refaça a configuração da API com "poetry run configure"')

    # garante que existe as chaves de API para conexão com Binance
    if not all([API_KEY, SECRET_KEY]):
        set_env(API_IS_CONFIGURED=0) # para facilitar a configuração
        env_logger().critical(f'Missing essential environment variables')
        raise ValueError('Faltam variáveis de ambiente essenciais. Refaça a configuração da API com "poetry run configure"')


    if API_KEY == 'NULL':
        API_KEY = ''

    if SECRET_KEY == 'NULL':
        SECRET_KEY = ''
        
    if DB_PASSWORD == 'NULL':
        DB_PASSWORD = ''


    # dados de configurações gerais
    TEST_MODE = os.getenv('TEST_MODE') == '1'
    DB_IS_CONFIGURED = os.getenv('DB_IS_CONFIGURED') == '1'
    API_IS_CONFIGURED = os.getenv('API_IS_CONFIGURED') == '1'

    _initialized = True
    encode_env()
    env_logger().info('Environment variables have been loaded')
    

# realiza a leitura inicial de .env
load_file_env()