import os
import logging
from logging.handlers import TimedRotatingFileHandler

# retorna o logger de configure
def config_logger():
    global _config_logger_initialized

    if not '_config_logger_initialized' in globals():
        _config_logger_initialized = False
    
    os.makedirs('./logs/', exist_ok=True)
    logger = logging.getLogger('config')

    if not _config_logger_initialized:
        handler = TimedRotatingFileHandler('./logs/config.log', when='midnight', interval=7, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        _config_logger_initialized = True

    return logger