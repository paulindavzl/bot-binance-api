# Guia de instalação (com exemplos de execução)

**OBS: tenha o _Docker_, _Poetry_ e o _MySQL_ (caso execute localmente) instalados.**

## Clone o repositório

```bash
git clone git@github.com:paulindavzl/bot-binance-api.git
```

### Instale as dependências

```bash
poetry install
```

**Obs: Esse comando somente será necessário caso você não for executar a API pelo Docker (não recomendado), caso contrário, as dependências são instaladas automáticamente!**

## Execute com Docker

É recomendado que todas as ações sejam realizadas com o contêiner Docker ativo!

```bash
docker-compose build
```

**Obs: Antes de executar o contêiner Docker, garanta que a porta 5000 esteja liberada.**

### Execute os testes

É recomendado que você execute os testes antes de prosseguir para garantir que está tudo funcionando e evitar problemas (executar testes fora de um contêiner pode resultar em exclusão de arquivos importantes):

```bash
docker-compose run tests
```

Caso não haja erros, prossiga para execução do servidor Flask, ativando o bot. No caso de erros, volte aqui para ver se já houve atualizações.

### Execução das configurações

```bash
docker-compose run configure
```

A configuração é obrigatória para iniciar o servidor, mas pode ser pulada usando o comando `--set dbs` e `--set api`. Veja [Comandos](COMMANDS.md)

### Execução do servidor

```bash
docker-compose run --service-ports api
```

Este comando ativará o bot localmente (http://127.0.0.1:5000/)

## Execute com Poetry

Executar diretamente com ambiente do Poetry pode ser que gere erros, para evitar isso execute com [Docker](#Execute-com-Docker)

Inicie o ambiente do Poetry com:

```bash
poetry shell
```

Execute os testes para garantir que não possui falhas:

```bash
poetry run tests
```

Após confirmar que está tudo rodando corretamente, inicie a configuração do bot, caso ocorra erros, tente executar com [Docker](#Execute-com-Docker) ativo ou verifique se há atuaizações.

Para configurar o bot execute o comando:

```bash
poetry run configure
```

Após configurar todas as informações para funcionamento do bot, você poderá iniciar o servidor com:

```bash
poetry run app
```

Garanta que a porta 5000 esteja disponível!

O servidor estará rodando localmente (http://127.0.0.1:5000/)

**Obs: É recomendado iniciar o servidor com [Docker](#Execute-com-Docker) para que não haja erros inesperados**

## Documentação

- [Visão geral](README.md)
- [Guia de comandos](docs/COMMANDS.md)
- [Guia de configuração](docs/CONFIGURATION.md)
- [Guia de endpoints](docs/ENDPOINTS.md)
