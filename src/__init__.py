from dotenv import load_dotenv
import os

# garante que .env exista
if not os.path.exists('.env'):
    with open('.env', 'w') as env:
        env.write('''
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=databse
DB_PORT=3306
''')

load_dotenv()

# dados para conexão com servidor MySQL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
