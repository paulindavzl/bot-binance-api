# Guia de configuração

Este é um guia de configuração, que visa explicar como fazer a configuração da API/bot por meio do prompt de comandos. Veja mais detalhes sobre os [comandos](COMMANDS.md "Guia de comandos"). Sempre confirmaremos tudo usando `-y`, mas tome cuidado para não executar algum comando indesejado! Não usaremos caractéres especiais (recomendo que não use também).

## Configuração do bot

A configuração do bot não é obrigatória e suas mudanças serão visíveis somente por meio de uma interface. Seus comandos são simples e poucos:

`--name` altera o nome do bot

`--adm` altera o administrador do bot

`--github` altera o GitHub do administrador do bot

`--debug` altera o modo do bot

`--emailaddress` define um e-mail

`--emailpass` define a senha do e-mail

`--certificate` gera um certificado TSL

Como usar:

```bash
--name CryptoSentinel --adm paulindavzl --github https://github.com/paulindavzl --debug off --emailaddress test00@example.com --emailpass your_password --certificate -y
```

**Este é um exemplo de como configurar o bot, troque somente para suas informações!**

## Configuração do banco de dados

A configuração do banco de dados é obrigatória, já que a API não pode ser inicada caso o banco de dados não estiver configurado!

`--user` define o usuário

`--host` define o servidor

`--pass` define a senha

`--port` define a porta

`--dbname` define o nome do banco de dados

Como usar:

```bash
--user root --host localhost --pass root --port 3306 --dbname database -y
```

**Este é um exemplo de como configurar o banco de dados, troque somente para suas informações**

**Caso não queira configurar o banco de dados (não recomendado), use `--set dbs` no prompt de comandos**

## Configuração da API Binance

A configuração da API [Binance](https://binance.com "Site da Binance") também é obrigatória e a API não pode ser iniciada se ela não estiver configurada!

`--accesskey` define a chave de acesso

`--secretkey` define a chave secreta

Como usar:

```bash
--accesskey your_access_key --secretkey your_secret_key -y
```

**Este é um exemplo de como configurar a API [Binance](https://binance.com "Site da Binance"), troque somente para suas informações**

**Caso não queira configurar a API [Binance](https://binance.com "Site da Binance") (não recomendado), use `--set api` no prompt de comandos**

## Documentação

- [Visão geral](../README.md "Visão geral")
- [Guia de instalação](INSTALL.md "Guia de instalação")
- [Guia de comandos](COMMANDS.md "Guia de comandos")
- [Guia de endpoints](docs/ENDPOINTS.md "Guia de endpoints")
- [Segurança](SECURITY.md)
