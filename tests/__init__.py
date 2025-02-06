import os
import logging
from src.config.parser import ParserError


logs = 'logs'
data = 'data'

def remove_files():

    logging.shutdown()

    # apaga todos os logs
    if os.path.exists(logs):
        logs_list = os.listdir(logs)
        for log in logs_list:
            if log != 'system.log':
                os.remove(f'{logs}/{log}')
    
    if os.path.exists(data):
        items_list = os.listdir(data)
        for item in items_list:
            os.remove(f'{data}/{item}')


def is_parser_error(obj: classmethod, name: str, item: str, typ: str) -> bool:
    if not all([isinstance(obj, ParserError), obj.name == name, obj.item == item, obj.typ == typ]):
        print(obj)
        return False
    return True


def is_restarted_system() -> bool:
    if os.path.exists(logs):
        log_list = os.listdir(logs)
        for log in log_list:
            if log != 'system.log':
                return False
        
    if os.path.exists(data):
        data_list = os.listdir(data)
        for item in data_list:
            if item != 'system.log':
                return False

    return True  


class Path:
    def __init__(self):
        self.cert = './data/cert.pem'
        self.key = './data/key.pem'


class FakeHandler:
    async def handler_DATA(self, server, session, envelope):
        return '250 Message accepted for delivery'