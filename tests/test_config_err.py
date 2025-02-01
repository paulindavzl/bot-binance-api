import re
import pytest
import src.__init__ as env
from src.config.err import show_error
from src.core.lang import langs
from utils import remove_files


@pytest.fixture
def restart_system():
    remove_files()
    yield
    remove_files()


# retorna uma classe de erro
@pytest.fixture
def err() -> classmethod:
    class Error: pass

    return Error


# retona langs já configure
def get_msg(lang, command, err_item):
    return re.escape(langs(env)[lang][command] + err_item)


# retorna show_error já configurado
def get_error(error):
    return re.escape(show_error(error, env))


# testa retornar todos as mensagens de command_error
def test_show_error_command_error(restart_system, err):
    err.name = 'command_error'
    err.item = '--command_test'

    # testa a mensagem em que o comando não existe
    err.typ = 'command'
    assert get_error(err) == get_msg('pt', 'COMMAND_ERROR', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'COMMAND_ERROR', err.item) # inglês

    # testa a mensagem em o comando é repetido
    err.typ = 'repeat'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'COMMAND_ERROR_REPEAT', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'COMMAND_ERROR_REPEAT', err.item) # inglês


# testa retornar todos as mensagens de value_error
def test_show_error_value_error(restart_system, err):
    err.name = 'value_error'
    err.item = '--value_test'

    # testa a mensagem em que o comando não aceita valor
    err.typ = 'bool'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'VALUE_ERROR_BOOL', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'VALUE_ERROR_BOOL', err.item) # inglês

    # testa a mensagem em o comando é está com valor vazio
    err.typ = 'empty'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'VALUE_ERROR_EMPTY', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'VALUE_ERROR_EMPTY', err.item) # inglês


# testa retornar todos as mensagens de type_error
def test_show_error_type_error(restart_system, err):
    err.name = 'type_error'
    err.item = '--type_test'

    # testa a mensagem em que o comando não pode ser usado junto de outro específico
    err.typ = 'command'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'TYPE_ERROR', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'TYPE_ERROR', err.item) # inglês

    # testa a mensagem em o comando --restart_system é usado junto de outro comando
    err.typ = 'restart'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'TYPE_ERROR_RESTART', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'TYPE_ERROR_RESTART', err.item) # inglês


# testa retornar todos as mensagens de sintaxe_error
def test_show_error_sintaxe_error(restart_system, err):
    err.name = 'sintaxe_error'
    err.item = '--sintaxe_test'

    # testa a mensagem em que o comando possui um caractére inválido
    err.typ = 'command'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'SINTAXE_ERROR', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'SINTAXE_ERROR', err.item) # inglês

    # testa a mensagem em que o comando está escrito errado ou não existe
    err.typ = 'invalid'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'SINTAXE_ERROR_INVALID', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'SINTAXE_ERROR_INVALID', err.item) # inglês

    # testa a mensagem em que o valor de um comando está escrito com caractéres inválidos
    err.typ = 'value'
    env.LANG = 'pt'
    assert get_error(err) == get_msg('pt', 'SINTAXE_ERROR_VALUE', err.item) # português
    env.LANG = 'en'
    assert get_error(err) == get_msg('en', 'SINTAXE_ERROR_VALUE', err.item) # inglês