from src.main import app
from src.config.check_system import is_ok

'''
facilita a execução do bot
a partir do ambiente do Poetry (poetry shell), execute: poetry run app
o bot é iniciado automaticamente quando Docker for executado. execute docker-compose build para construir o contêiner e docker-compose up para executá-lo
'''

def run():
    if not is_ok():
        print('Ocorreu um erro ao verificar o sistema. Verifique o arquivo check.log (logs/check.log) para ver mais detalhes da falha!')
        return

    app.run(host='0.0.0.0', port=5000, debug=True)