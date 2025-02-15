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


# testa enviar um email sem ter feito a configurção
def test_send_email_email_not_configured():
    remove_files() # apaga os arquivos

    response = SendEmail(
        env=env,
        to='test@test.com',
        subject='Testing',
        content='This is a test'
    )

    assert not response.status
    assert response.error == 'email_not_configured'


# testa enviar um email
def test_send_email(start_server):
    response = SendEmail(
        env=env,
        to='test@test.com',
        subject='Testing',
        content='This is a test',
        server='localhost:1025'
    )

    assert response.status
    assert not response.error


# testa enviar um email com as credenciais inválidas
def test_send_email_invalid_credentials():
    response = SendEmail(
        env=env,
        to='test@test.com',
        subject='Testing',
        content='This is a test'
    )

    assert not response.status
    assert response.error == 'invalid_credentials'
