import pytest
import asyncio
from aiosmtpd.controller import Controller
import src.__init__ as env
from src.core.emails.manager import SendEmail
from tests import remove_files, FakeHandler

@pytest.fixture(scope='module')
def start_server():
    remove_files()
    env.load_file_env(True)
    env.set_env(EMAIL_ADDRESS='test@test.com', EMAIL_PASSWORD='test')

    controller = Controller(FakeHandler(), hostname='localhost', port=1025)
    controller.start()

    yield
    
    controller.stop()
    remove_files()


# testa enviar um email
def test_send_email(start_server):
    result = SendEmail(env,
        to='test@test.com',
        subject='Testing',
        content='This is a test',
        server='localhost:1025'
    )

    assert result.status