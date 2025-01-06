import os
import json
import pytest
from src.config import configure as cfg 


# testa carregar o arquivo de configuração
def test_hide_password():
    pass1 = cfg.hide_password('test123')
    pass2 = cfg.hide_password('tes')
    pass3 = cfg.hide_password('')

    assert pass1 == 't*****3'
    assert pass2 == '***'
    assert pass3 == ''