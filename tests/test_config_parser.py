import pytest
from src.config.parser import Parser, ParserError
import src.__init__ as env
from utils import is_parser_error


# testa separar os comandos
def test_parser():
    cmd_line = '--user root --host localhost'
    result = Parser(cmd_line).result

    assert result == {'--user': 'root', '--host': 'localhost', '-y': False, '-n': False}


# testa usar --restart_system com outro comando
def test_parser_type_error_restart_system():
    cmd_line = '--restart_system --user root'
    result = Parser(cmd_line).result.get('err')

    assert is_parser_error(result, 'type_error', '--user', 'restart')


# testa passar -y (confirma tudo) e -n (nega tudo) juntos
def test_parser_type_error_y_n():
    cmd_line = '--restart_system -y -n'
    result = Parser(cmd_line).result.get('err')

    assert is_parser_error(result, 'type_error', '-y & -n', 'command')


# tenta passar um comando inválido, que não existe
def test_parser_command_error_command():
    cmd_line = '--usr root'
    result = Parser(cmd_line).result.get('err')
    
    assert is_parser_error(result, 'command_error', '--usr', 'command')


# tenta repetir um comando na mesma linha
def test_parser_command_error_repeat():
    cmd_line = '--user root --user toor'
    result = Parser(cmd_line).result.get('err')
    
    assert is_parser_error(result, 'command_error', '--user', 'repeat')


# tenta passar valores em comando que não aceitam (--restart_system, -y e -n)
def test_parser_value_error_bool():
    cmd_line1 = '--restart_system yes'
    result1 = Parser(cmd_line1).result.get('err')

    cmd_line2 = '-y yes'
    result2 = Parser(cmd_line2).result.get('err')

    cmd_line3 = '-n no'
    result3 = Parser(cmd_line3).result.get('err')
    
    assert is_parser_error(result1, 'value_error', '--restart_system', 'bool')
    assert is_parser_error(result2, 'value_error', '-y', 'bool')
    assert is_parser_error(result3, 'value_error', '-n', 'bool')


# tenta não passar valor para um comando que exige
def test_parser_value_error_empty():
    cmd_line = '--user --host localhost'
    result = Parser(cmd_line).result.get('err')

    assert is_parser_error(result, 'value_error', '--user', 'empty')


# tenta passar um comando que não inicia com -- ou - (apenas -y e -n)
def test_parser_sintaxe_error_invalid():
    cmd_line = '-user root'
    result = Parser(cmd_line).result.get('err')

    assert is_parser_error(result, 'sintaxe_error', '-user', 'invalid')


# testa passar o valor de um comando com caractéres inválidos
def test_parser_sintaxe_error_value():
    cmd_line = fr'--user r\oot'
    result = Parser(cmd_line).result.get('err')

    assert is_parser_error(result, 'sintaxe_error', '--user', 'value')
