import os
import time
from cryptography.fernet import Fernet, InvalidToken


# altera a chave
def change_key(env):
    '''script para alterar a chave
    use seu próprio mecanismo, ele deve ter alterar a chave principal a depois do tempo em TIME_CHANGE_BACKUP_KEY (segundos) deve alterar a chave de backup
    
    Parâmetros:
        env: carrega informações como TIME_CHANGE_BACKUP_KEY, env_logger e outras (veja src/__init__.py)'''

    # altere se necessário
    default_mechanism_change_key(env) # altera a chave pela forma padrão


# obtém a chave de decodificação
def get_key(env, backup: bool=False, generate_backup: bool=True) -> str:
    '''script para obter a chave de decodificação (principal e backup)
    use seu próprio mecanismo, ele deve gerar uma chave principal e de backup e retorná-las quando necessário. SEMPRE DEVE RETORNAR UMA CHAVE STR
    
    Parâmetros:
        env: carrega informações como TIME_CHANGE_BACKUP_KEY, env_logger e outras (veja src/__init__.py)
        backup: indica se a chave é questão é a de backup ou a principal
        generate_backup: indica se é para gerar backup ou não'''

    # altere se necessário
    key = default_mechanism_get_key(env, backup=backup, generate_backup=generate_backup) # gera e obtém uma chave (principal ou de backup)

    return key


# mecanismo padrão para alterar a chave
def default_mechanism_change_key(env):
    if os.path.exists(env.PATH_KEY):
        os.remove(env.PATH_KEY)
    
    get_key(env=env) # chama get_key somente para gerar uma nova chave
    env.env_logger().info('The key in .key has been changed')

    time.sleep(float(env.TIME_CHANGE_BACKUP_KEY)) # espera o tempo definido para trocar o backup da chave

    if os.path.exists(env.PATH_BACKUP):
        os.remove(env.PATH_BACKUP)
    
    get_key(backup=True, env=env)
    env.env_logger().info('The key in backup.key has been changed')


# mecanismo padrão para obter a chave de decodificação
def default_mechanism_get_key(env, backup: bool=False, generate_backup: bool=True) -> str:
    key = ''
    file_key = env.PATH_BACKUP if backup else env.PATH_KEY

    # garante que .key exista
    if not os.path.exists(file_key):
        if backup:
            if not os.path.exists(env.PATH_KEY):
                get_key(generate_backup=False, env=env)
            with open(env.PATH_KEY, 'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()

        with open(file_key, 'wb') as file:
            file.write(key)
        
        if generate_backup and not backup:
            get_key(backup=True, env=env)

        env.env_logger().info(f'The {'backup' if backup else ''}.key file has been created') # carrega um log
    
    with open(file_key, 'rb') as file:
        key = file.read()
    
    return key