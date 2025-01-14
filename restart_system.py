import os
import logging

def run():
    logs = './logs'
    enc = './.enc'
    env = './.env'
    key = './.key'

    os.system('cls' if os.name == 'nt' else 'clear')

    restart_pass = 'RESTART SYSTEM'
    response = input(f'Confirme que você quer reiniciar todo o sistema para configuração inicial.\nIsso apagará todos os arquivos contidos em logs/, os arquivos .env, .enc e .key também serão apagados!\nDigite: {restart_pass}\n>>')
    if response == restart_pass:
        logging.shutdown()

        # apaga todos os logs
        if os.path.exists(logs):
            logs_list = os.listdir(logs)
            for log in logs_list:
                os.remove(f'{logs}/{log}')
        
        # apaga .key 
        if os.path.exists(key):
            os.remove(key)
        
        # apaga .enc 
        if os.path.exists(enc):
            os.remove(enc)

        # apaga .env 
        if os.path.exists(env):
            os.remove(env)
        input('Todo o sistema foi restaurado para a configuração inicial.\nNote que informações contidas em bancos de dados continuam inalteradas!\nAltere manualmente se necessário.\nENTER para finalizar!')
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()
    
    input('Restauração cancelada!\nENTER para cancelar')
    os.system('cls' if os.name == 'nt' else 'clear')