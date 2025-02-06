import os
import pytest
from unittest.mock import patch
import src.__init__ as env
from src.config.certificate import gen_certificate
from tests import remove_files, Path

@pytest.fixture
def restart_system():
    remove_files()
    env.load_file_env(True)
    yield
    remove_files()


@pytest.fixture
def path() -> Path:
    return Path()


# testa gerar um certificado
def test_gen_certificate(restart_system, path):
    # garante que os certificados não existem
    assert not all([os.path.exists(path.cert), os.path.exists(path.key)])

    gen_certificate(env) # gera os certificados

    # verifica se os certificados foram criados
    assert all([os.path.exists(path.cert), os.path.exists(path.key)])


# testa tentar gerar um certificado já tendo um
def test_gen_certificate_certificate_exists(restart_system, path):
    gen_certificate(env) # gera os certificados
    assert all([os.path.exists(path.cert), os.path.exists(path.key)]) # verifica se os certificados foram criados

    result = gen_certificate(env)

    assert result == 'certificate_exists'


# testa confirmar a geração de um novo certificado porque o atual está incompleto
def test_gen_certificate_certificate_incomplete_confirmed(restart_system, path):
    gen_certificate(env) # gera os certificados
    assert all([os.path.exists(path.cert), os.path.exists(path.key)]) # verifica se os certificados foram criados

    os.remove(path.cert) # remove cert.pem

    assert not os.path.exists(path.cert)

    with patch('builtins.input', return_value='y'):
        gen_certificate(env)

    assert all([os.path.exists(path.cert), os.path.exists(path.key)]) # verifica se os certificados foram criados


# testa negar a geração de um novo certificado porque o atual está incompleto
def test_gen_certificate_certificate_incomplete_denied(restart_system, path):
    gen_certificate(env) # gera os certificados
    assert all([os.path.exists(path.cert), os.path.exists(path.key)]) # verifica se os certificados foram criados

    os.remove(path.cert) # remove cert.pem

    assert not os.path.exists(path.cert)

    result = ''
    with patch('builtins.input', return_value='n'):
        result = gen_certificate(env)

    assert [os.path.exists(path.cert), os.path.exists(path.key)] == [False, False]
    assert result == 'new_certificate_denied'
