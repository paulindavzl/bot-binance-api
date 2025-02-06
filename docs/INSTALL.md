# Guia de instalação (com exemplos de execução)

**OBS: tenha o _Docker_, _Poetry_ e o _MySQL_ (caso execute localmente) instalados.**

## Clone o repositório

```bash
git clone git@github.com:paulindavzl/bot-binance-api.git
```

## Execute com Docker

Não é possível executar esta API se não for por meio dos comandos abaixo:

```bash
docker-compose build
```

**Obs: Antes de executar o contêiner Docker, garanta que a porta 5000 e 8200 esteja liberada.**

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

A configuração é obrigatória para iniciar o servidor, mas pode ser pulada usando o comando `--set dbs` e `--set api`. Veja mais detalhes em [Comandos](COMMANDS.md "Guia de comandos")

### Execução do servidor

```bash
docker-compose run --service-ports api
```

Este comando ativará o bot localmente (http://127.0.0.1:5000/)

## Documentação

- [Visão geral](../README.md "Visão geral")
- [Guia de comandos](COMMANDS.md "Guia de comandos")
- [Guia de configuração](CONFIGURATION.md "Guia de configuração")
- [Guia de endpoints](docs/ENDPOINTS.md "Guia de endpoints")
- [Segurança](SECURITY.md)
