import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from src import DB_USER, DB_HOST, DB_PORT, DB_PASSWORD, DB_NAME
from src.main import app


# retorna o logger de modals
def modals_logger():
    os.makedirs('./logs/', exist_ok=True)
    logger = logging.getLogger('modals')

    if not logger.hasHandlers():
        handler = TimedRotatingFileHandler('./logs/modals.log', when='midnight', interval=1, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# verifica se a conexão com o banco de dados ou API foi bem sucedida
def is_connected(connect_in: str='db') -> bool:
    if connect_in == 'db':
        try:
            db.session.execute('SELECT 1;')
            return True
        except:
            modals_logger().critical('Unable to connect to database')
            return False
    return True