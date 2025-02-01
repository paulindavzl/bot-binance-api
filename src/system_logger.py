import os
import logging
from logging.handlers import TimedRotatingFileHandler

# retorna o logger do sistema (marca iniciações e erros (CRITICAL) gerais)
def sys_logger():
    os.makedirs('./logs/', exist_ok=True)
    logger = logging.getLogger('system')

    if not logger.hasHandlers():
        handler = TimedRotatingFileHandler('./logs/system.log', when='midnight', interval=7, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger