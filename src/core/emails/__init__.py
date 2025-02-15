import os
import logging
from logging.handlers import TimedRotatingFileHandler

# retorna o logger de email
def email_logger():
    os.makedirs('./logs/', exist_ok=True)
    logger = logging.getLogger('email')

    if not logger.hasHandlers():
        handler = TimedRotatingFileHandler('./logs/emails.log', when='midnight', interval=7, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger