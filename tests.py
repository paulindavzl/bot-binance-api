import pytest

'''
facilita a execução dos testes pelo Poetry
a partir do ambiente do Poetry (poetry shell) execute: poetry run tests
'''

def run():
    pytest.main(['tests/', '-vv'])