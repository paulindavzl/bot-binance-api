from src import FLASK_DEBUG
from src.main import app

'''
facilita a execução do bot
a partir do ambiente do Poetry (poetry shell), execute: poetry run app
o bot é iniciado automaticamente quando Docker for executado. execute docker-compose build para construir o contêiner e docker-compose up para executá-lo
'''

def run():
    app.run(host='0.0.0.0', port=5000, debug=True if FLASK_DEBUG == 1 else False)