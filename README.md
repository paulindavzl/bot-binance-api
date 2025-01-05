# CryptoSentinel

API/bot que conecta e realiza operações em criptomoedas por meio de APIs da [Binance](https://binance.com/).

## Dependências

<a href="https://www.docker.com/" target="_blank"><img src="https://github.com/user-attachments/assets/94c615fb-79d1-46b3-848e-667f9e312716" alt="Docker" width="130" height="130" title="usa Docker para manter a consistência do projeto em todas as máquinas"></a>
<a href="https://python-poetry.org/docs/" target="_blank"><img src="https://github.com/user-attachments/assets/5be6ef37-662a-4319-8a7f-f0ed1b15ba37" alt="Poetry" width="130" height="130" title="usa Poetry para gerenciar dependências"></a>
<a href="https://flask.palletsprojects.com/en/stable/installation/" target="_blank"><img src="https://github.com/user-attachments/assets/034ef091-fb20-4193-8945-71dd748b053c" alt="Flask" width="130" height="130" title="usa Flask para criar a API"></a>
<a href="https://www.mysql.com/downloads/" target="_blank"><img src="https://github.com/user-attachments/assets/629d1c03-6807-48d5-9fa5-6e12b3446e1e" alt="MySQL" width="130" height="130" titlle="usa MySQL como SGDB"></a>

O **Flask** é uma dependência que é instalada automaticamente, mas caso você não tenha o **Poetry**, **Docker** ou **MySQL** (caso execute localmente), veja como instalá-los clicando em seus logos acima.

Este projeto também utiliza, para se conectar com banco de dados, uma ORM própria! Saíba mais em [MyORM](https://github.com/paulindavzl/my-orm/)

## Instalação

**OBS: tenha o _Docker_, _Poetry_ e o _MySQL_ (caso execute localmente) instalados.**

### Clone o repositório

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

É recomendado que você execute os testes antes de prosseguir para garantir que está tudo funcionando e evitar problemas:

```bash
docker-compose run tests
```

Caso não haja erros, prossiga para execução do servidor Flask, ativando o bot. No caso de erros, volte aqui para ver se já houve atualizações.

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

**Obs: É recomendado iniciar o servidor com [Docker](#Execute-com-Docker) para que não haja erros inesperados!**