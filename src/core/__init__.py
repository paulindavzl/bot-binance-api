import logging

# retorna o logger de core
@property
def core_logger():
    global _logger_initialized

    if not '_logger_initialized' in globals():
        _logger_initialized = False
    
    logger = logging.getLogger('core')

    if not _logger_initialized:
        handler = logging.FileHandler('./logs/core.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        _logger_initialized = True

    return logger
