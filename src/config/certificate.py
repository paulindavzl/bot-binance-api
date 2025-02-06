import os
import subprocess
from src.config import config_logger
from src.core.lang import path, langs
from src.core.utils import wait, clear

# gera certificado TLS
def gen_certificate(env):
    if not os.path.exists('./data'):
        os.makedirs('./data')

    key_path = './data/key.pem'
    cert_path = './data/cert.pem'

    # certificado já existe
    if os.path.exists(key_path) and os.path.exists(cert_path):
        env.set_env(CERTIFICATE=True)
        config_logger().info('The TSL certificate already exists!')
        clear(langs(env)[env.LANG]['CERTIFICATE_EXISTS'])
        return 'certificate_exists'
    
    # certificado incompleto
    elif os.path.exists(key_path) or os.path.exists(cert_path):
        env.set_env(CERTIFICATE=False)
        config_logger().warning('The TSL certificate is incomplete.')
        while True:
            clear(langs(env)[env.LANG]['CERTIFICATE_INCOMPLETE'])
            response = input(f'{path(env)} ')

            if response == 'y':
                config_logger().info('Permission to generate another certificate confirmed')
                if os.path.exists(key_path): os.remove(key_path)
                if os.path.exists(cert_path): os.remove(cert_path)
                break
            elif response == 'n':
                config_logger().warning('Permission to generate another certificate denied')
                if os.path.exists(key_path): os.remove(key_path)
                if os.path.exists(cert_path): os.remove(cert_path)
                return 'new_certificate_denied'
            else:
                clear(f'{path} {response}')
                print(f'{langs(env)[env.LANG]['INVALID_RESPONSE']} [y/n]')
                wait(env, langs)

    try:
        subprocess.run(['openssl', 'version'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        config_logger().error('Unable to generate TSL certificate because OpenSSL is not installed!')
        clear(langs(env)[env.LANG]['OPENSSL_UNINSTALED'])
        env.set_env(CERTIFICATE=False)
        return
    
    result = subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:4096', 
        '-keyout', key_path, '-out', cert_path,
        '-days', '365', '-nodes', '-subj', '/CN=localhost'
    ])

    if result.returncode == 0:
        clear(langs(env)[env.LANG]['CERTIFICATE_GENERATED'])
        env.set_env(CERTIFICATE=True)
    else:
        config_logger().error(f'An error occurred when trying to generate the TSL certificate:{result.stderr}')
        clear(f"{langs(env)[env.LANG]['CERTIFICATE_GENERATED_FAILED']}\n{result.stderr}")
        env.set_env(CERTIFICATE=False)