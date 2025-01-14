import os
import time
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key


# altera o tempo de troca das chaves
def set_time_change_key(tck: [int, float]=60, tcbk: [int, float]=10, reset: bool=False):
    global _time_change_key_defined

    if not '_time_change_key_defined' in globals():
        _time_change_key_defined = False

    if _time_change_key_defined or not reset:
        return

    TIME_CHANGE_KEY = float(tck) * 60
    TIME_CHANGE_BACKUP_KEY = float(tcbk) * 60

    env_logger().info(f'The decryption key exchange time has been set to: "{TIME_CHANGE_KEY}" seconds ("{tck}" minutes)')
    env_logger().info(f'Decryption key backup exchange time has been set to: "{TIME_CHANGE_BACKUP_KEY}" seconds ("{tcbk}" minutes)')

    _time_change_key_defined = True


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
    if not os.path.exists('.env'):
        with open('.env', 'w'):
            pass

    set_env(
            reload=False,

            # define informações de conexão com banco de dados
            DB_USER='root',
            DB_PASSWORD='NULL',
            DB_NAME='database',
            DB_HOST='localhost',
            DB_PORT=3306,

            # define o tempo de  troca de chaves
            TIME_CHANGE_KEY = 60 * 60,
            TIME_CHANGE_BACKUP_KEY = 10 * 60,

            # define informações de conexão com a Binance (indefinidas por padrão)
            ACCESS_KEY='NULL',
            SECRET_KEY='NULL',

            # define informações de configurações gerais
            DB_IS_CONFIGURED=0,
            API_IS_CONFIGURED=0
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

    time.sleep(float(TIME_CHANGE_BACKUP_KEY))

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
        decode_env()

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

    if not os.path.exists('.enc') and not os.path.exists('.env'):
        set_default_env()
    elif os.path.exists('.env'):
        return

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
        if os.getenv(key) != envs[key]:
            set_key('.env', key, str(envs[key]))
            env_logger().info(f'The environment variable "{key}" has been assigned the value "{envs[key]}"')
    
    # recarrega as variáveis de ambiente
    if reload:
        load_file_env(True)

    encode_env()


# carrega as variáveis de ambiente
def load_file_env(reload: bool=False):
    global _initialized
    global DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
    global TIME_CHANGE_KEY, TIME_CHANGE_BACKUP_KEY
    global ACCESS_KEY, SECRET_KEY, DB_IS_CONFIGURED, API_IS_CONFIGURED

    # caso _initialized não esteja definido
    if not '_initialized' in globals():
        _initialized = False

    # impede que .env fique sendo aberto, decodificado e codificado a todo momento
    if _initialized and not reload:
        return
        
    # garante que .env exista
    if not os.path.exists('.enc') and not os.path.exists('.env'):
        set_default_env(True)
        encode_env()
    
    decode_env()
    load_dotenv()

    # dados para conexão com servidor MySQL
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = int(os.getenv('DB_PORT', 3306))

    # tempo de troca de chaves
    TIME_CHANGE_KEY = os.getenv('TIME_CHANGE_KEY')
    TIME_CHANGE_BACKUP_KEY = os.getenv('TIME_CHANGE_BACKUP_KEY')

    # dados para conexão com Binance
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # garante que existe as informações de conexão com o banco de dados
    db_variables = {'DB_HOST':DB_HOST, 'DB_NAME':DB_NAME, 'DB_PORT':DB_PORT, 'DB_USER':DB_USER, 'DB_PASSWORD':DB_PASSWORD}
    if not all([DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_PORT]):
        missing = []
        for i in db_variables:
            if db_variables[i] is None:
                missing.append(i)
        set_env(DB_IS_CONFIGURED=0, reload=False) # para facilitar a configuração
        env_logger().critical(f'Missing essential environment variables: {missing}')
        raise ValueError('Essential environment variables are missing. Redo the API configuration with "poetry run configure"')

    # garante que existe as chaves de API para conexão com Binance
    api_variables = {'ACESS_KEY': ACCESS_KEY, 'SECRET_KEY': SECRET_KEY}
    if not all([ACCESS_KEY, SECRET_KEY]):
        missing = []
        for i in api_variables:
            if api_variables[i] is None:
                missing.append(i)
        set_env(API_IS_CONFIGURED=0, reload=False) # para facilitar a configuração
        env_logger().critical(f'Missing essential environment variables: {missing}')
        raise ValueError('Essential environment variables are missing. Redo the API configuration with "poetry run configure"')

    if ACCESS_KEY == 'NULL':
        ACCESS_KEY = ''

    if SECRET_KEY == 'NULL':
        SECRET_KEY = ''
        
    if DB_PASSWORD == 'NULL':
        DB_PASSWORD = ''


    # dados de configurações gerais
    DB_IS_CONFIGURED = os.getenv('DB_IS_CONFIGURED') == '1'
    API_IS_CONFIGURED = os.getenv('API_IS_CONFIGURED') == '1'

    _initialized = True
    encode_env()
    env_logger().info('Environment variables have been loaded')
    

# realiza a leitura inicial de .env
try:
    set_time_change_key()
    load_file_env()
except Exception as e:
    env_logger().critical(f'Unexpected error: {traceback.format_exc()}')
    raise e
