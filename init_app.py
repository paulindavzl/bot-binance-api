import traceback
import src.__init__ as env
from src.main import app
from src.system_logger import sys_logger
from src.config import check_system
from src.core.emails.manager import SendEmail

'''
facilita a execução do bot
a partir do ambiente do Poetry (poetry shell), execute: poetry run app
o bot é iniciado automaticamente quando Docker for executado. execute docker-compose build para construir o contêiner e docker-compose up para executá-lo
'''

def run():
    try: 
        HOST = '127.0.0.1'
        PORT = 5000
        sys_logger().info(f'API started.\n\tHOST: {HOST}\n\tPORT: {PORT}\n\tDEBUG: {str(env.DEBUG)}')

        if not check_system.is_ok():
            sys_logger().critical('Failed to start API: System has not been configured')
            raise SystemError('Failed to start API: System has not been configured. Use docker-compose run configure/poetry run configure')

        app.run(host=HOST, port=PORT, debug=env.DEBUG)
    except Exception as e:
        sys_logger().critical(f'A critical error has occurred:\n\t{traceback.format_exc()}')
        SendEmail(
            env=env,
            subject='critical_error',
            to=env.EMAIL_ADDRESS,
            content=traceback.format_exc(),
            system=True
        )
        raise e