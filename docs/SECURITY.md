[HashiCorp Vault](https://www.hashicorp.com/products/vault "Site da HashiCorp")

# Informações de segurança

Esta API/bot conta com um sistema que foca em manter a segurança do usuário.

## Variáveis de ambiente

As **variáveis de ambiente** são criptografadas usando o mecanismo **AES-128-CBC** e contam com uma proteção de integridade **HMAC-SHA256**, que garante que os dados não foram corrompidos.

O sistema gera duas chaves (uma principal e uma de backup) e às armazena localmente, isso pode ser um problema dependendo de quem tem acesso ao ambiente que a API está sendo executada, já que se as chaves vazarem **as informações estarão comprometidas!**

Caso queira aumentar a segurança, você pode implementar seu próprio mecanismo para proteger as chaves. Isso pode ser feito modificando apenas duas funções:

```python
# bot-binance-api/src/key_mechanism.py

import os
import time
from cryptography.fernet import Fernet, InvalidToken


# altera a chave
def change_key(env):
    '''script para alterar a chave
    use seu próprio mecanismo, ele deve ter alterar a chave principal a depois do tempo em TIME_CHANGE_BACKUP_KEY (segundos) deve alterar a chave de backup
  
    Parâmetros:
        env: carrega informações como TIME_CHANGE_BACKUP_KEY, env_logger e outras (veja src/__init__.py)'''

    # altere se necessário
    default_mechanism_change_key(env) # altera a chave pela forma padrão


# obtém a chave de decodificação
def get_key(env, backup: bool=False, generate_backup: bool=True) -> str:
    '''script para obter a chave de decodificação (principal e backup)
    use seu próprio mecanismo, ele deve gerar uma chave principal e de backup e retorná-las quando necessário. SEMPRE DEVE RETORNAR UMA CHAVE STR
  
    Parâmetros:
        env: carrega informações como TIME_CHANGE_BACKUP_KEY, env_logger e outras (veja src/__init__.py)
        backup: indica se a chave é questão é a de backup ou a principal
        generate_backup: indica se é para gerar backup ou não'''

    # altere se necessário
    key = default_mechanism_get_key(env, backup=backup, generate_backup=generate_backup) # gera e obtém uma chave (principal ou de backup)

    return key
```

Tudo que você deve modificar é o **script** dentro de `change_key()` e `get_key()`, usando os parâmetros que já vem. **Não adicione novos parâmetros ou remova os existentes!** Você encontrará estas funções no caminho **`src/key_mechanism.py`**, lá possui outras funções, **NÃO MODIFIQUE-AS!**

As chaves possuem uma rotação padrão, sendo trocadas a cada 3600 segundos (1 hora). Cada vez que a chave principal é trocada, a chave de backup aguarda 600 segundos (10 minutos) antes de ser trocada, esse tempo garante que todo o sistema mude para a nova chave.

## LOGS

A API/bot conta com um sistema de **LOGS** que registram todas as operações internas e armazena-os em um diretório local. Isso permite monitorar seu funcionamento, identificar e tratar erros.

LOGS de `erros críticos` são informados em um **email** que pode ser cadastrado pelo [prompt de comandos](COMMANDS.md "Guia de comandos").

Todos os LOGS podem ser acessados através do diretório `logs/`, localizado na **raiz do projeto**.

## Certificado TSL

Você poderá gerar um **Certificado TSL Autoassinado**. Este certificado criptografa os dados transmitidos entre servidor e cliente, o que garante a sua segurança, autenticidade e integridade. Com um **Certificado TSL** gerado, automaticamente o sistema identifica e passa de **`HTTP`** para **`HTTPS`**.

O **Certificado TSL** pode ser gerado por meio do [prompt de comandos](COMMANDS.md "Guia de comandos"). Uma vez gerado não poderá gerar outro, a não ser que o atual seja apagado ou esteja incompleto.
