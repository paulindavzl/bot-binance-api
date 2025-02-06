import pytest
import src.__init__ as env
from tests import remove_files
from src.config import check_system

@pytest.fixture
def restart_system():
    remove_files()
    env.load_file_env(True)
    yield
    remove_files()


# testa se a verificação do sistema
def test_is_ok(restart_system):
    assert not check_system.is_ok()
    
    # simula a configuração do sistema
    env.set_env(API_IS_CONFIGURED=True, DB_IS_CONFIGURED=True)

    assert check_system.is_ok()