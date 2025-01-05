from src.main import app

'''
facilita a execução do bot
a partir do ambiente do Poetry (poetry shell), execute: poetry run app
o bot é iniciado automaticamente quando Docker for executado. execute docker-compose build para construir o contêiner e docker-compose up para executá-lo
Obs: o bot é iniciado no modo debug. defina-o como False para mudar isso
'''

def run():
    app.run(debug=True, host='0.0.0.0', port=5000)