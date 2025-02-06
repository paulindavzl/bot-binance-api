# Guia de comandos

Guia de comandos com exemplos simples. Para ver exemplos mais complexos veja [Guia de configuração](CONFIGURATION.md "Guia de configuração").

- `--help` mostra todos os comandos com exemplos de uso.
- `--lang` altera o idioma do prompt, podendo ser `português` (padrão) ou `inglês`

  ```bash
  --lang pt # define para português
  --lang en # define para inglês
  ```

  Qualquer valor diferente desses é convertido para `pt`.

## Informações do bot

Comandos usados para definir informações do bot (nome, administrador, GitHub do administrador e modo Debug).  Note que essas informações ficam disponíveis, visivelmente, na inteface WEB ou por [endpoints](ENDPOINTS.md "Guia de endpoints").

- `--name` altera o nome do bot

  ```bash
  --name bot_name
  --name "bot name"
  ```
- `--adm` altera o administrador do bot

  ```bash
  --adm adm_name
  --adm "adm name"
  ```
- `--github` altera o GitHub do administrador do bot

  ```bash
  --github https://github.com/username
  ```
- `--certificate` gera um **Certificado TSL**

  ```bash
  --certificate
  ```
- `--emailaddress` define um email, onde será enviados **`logs`** e outras informações importantes

  ```bash
  --emailaddress your_email_address@example.com
  ```
- `--emailpass` define a senha para permitir que o email seja enviado. Note que a senha em questão não é senha que você define ao criar o email. Esta senha é a chamada **`senha de app`.** [Clique aqui](https://support.google.com/accounts/answer/185833?hl=pt-BR "Fazer login com senhas de app") para saber mais.

  ```bash
  --emailpass your_app_password
  ```
- `--sendemail` envia um email para o destinatário informado, serve para testar se o cadastro foi bem sucessido.

  ```bash
  --sendemail your_other_email@example.com
  ```
- `--debug` altera o modo de operação do bot (não muda nada significamente, mas toda alteração manual dos arquivos será refletida automaticamente ao bot)

  ```bash
  --debug on # define como ligado (padrão)
  --debug off # define como desligado
  ```

  Qualquer valor diferente desses é convertido para `on`.

## Banco de dados

Comandos usados para definir os dados do banco de dados (usuário, servidor, senha, porta e nome do banco de dados). Esta etapa é obrigatória para iniciar a API, mas pode ser pulada com o uso do comando `--set dbs`. O banco de dados vem configurado com informações para conectar-se com um servidor local:

```bash
user: root
host: localhost
password: '' (sem senha)
port: 3306
database name: database
```

Veja agora os comandos para alterar essas informações:

- `--user` altera o usuário

  ```bash
  --user username
  ```
- `--host` altera o servidor

  ```bash
  --host https://your_host_url.example
  ```
- `--pass` altera a senha

  ```bash
  --pass your_password123
  --pass "@your password 123"
  ```
- `--port` altera a porta (geralmente a porta padrão de servidores MySQL é 3306)

  ```bash
  --port 3306
  ```

  **Qualquer valor que não seja inteiro resultará em erro!**
- `--dbname` altera o nome do banco de dados

  ```bash
  --dbname your_database_name
  --dbname "your database name"
  ```

## API Binance

Comandos para definir as informações para conexão com API da [Binance](https://binance.com "Site da Binance") (chave de acesso e chave secreta). Esta etapa também é obrigatória para iniciar a API, mas pode ser pulada usando o comando `--set api`.

- `accesskey` altera a chave de acesso da [Binance](https://binance.com "Site da Binance")

  ```bash
  --accesskey your_access_key
  ```
- `secretkey` altera a chave secreta da [Binance](https://binance.com "Site da Binance")

  ```bash
  --secretkey your_secret_key
  ```

## Outros comandos

### Tempo de troca de chaves

Comandos utilizados para alterar o tempo de troca das chaves de decodificação (principal e backup). Note que os valores devem ser inteiros ou decimais separados por um ponto (.), caso contrário resultará em erro!

- `timekey` altera o tempo de troca da chave principal em segundos (por padrão é de 3600 segundos)

  ```bash
  --timekey 3600.0
  ```
- `timebackup` altera o tempo de troca da chave de backup em segundos (por padrão é de 600 segundos)

  ```bash
  --timebackup 600.0
  ```

### Restaurar informações

Este comando é utilizado para restaurar todas as informações da API/bot para o padrão. Note que isso apagará todos os dados **LOCAIS**, e dados em bancos de dados serão mantidos!

- `--restart_system` inicia a restauração do sistema

  ```bash
  --restart_system
  --restart_system --cmd # causará erro
  --restart_system value # causará erro
  ```

  `--restart_system` não pode receber valor e ser usado junto de outro comando, exceto `-y` ou `-n`, caso contrário resultará em erro.

## Nota

### Email e senha

O email cadastrado deve ver **Gmail**, caso contrário resultará em erro.

A senha cadastrada deve ser a chamada **senha de app**. [Clique aqui](https://support.google.com/accounts/answer/185833?hl=pt-BR "Fazer login com senhas de app") para saber mais.

### Caractéres especiais

Para usar qualquer caractére especial ou espaços em branco nos valores dos comandos, use aspas simples ou duplas, caso contrário resultará em erro.

```bash
--cmd "your value"
--cmd 'your value'
--cmd your value # causará erro
```

### Automatizar confirmação

Todos os comandos antes de serem executados pedem uma confirmação (`y` ou `n`), para pular esta etapa use `-y` para confirmar todos ou `-n` para negar todos. Estes não podem ser usados juntos na mesma linha de comando e nem receber qualquer valor, caso contrário resultará em erro.

```bash
--cmd -y
--cmd -n
--cmd -y -n # causará erro
```

### Vários comandos juntos

Você pode usar vários comandos de uma vez, desde que possam ser usados assim.

```bash
--name bot_name --adm adm_name --github https://github.com/username -y
```

### Exigência de valores

Com exceção dos comandos `--restart_system`, `-y` e `-n`, todos os comandos exigem um valor, caso contrário resultará em erro.

```bash
--name bot_name --adm adm_name
--name --adm_name # causará erro
```

### Pular configuração

A configuração inical é obrigatória, mas pode ser pulada com uso do comando `--set`

```bash
--set dbs # define o banco de dados como configurado
--set api # define a API da Binance como configurada
```

Caso o banco de dados e a API da [Binance](https://binance.com "Site da Binance") não tiverem o status de `configurado`, não será possível iniciar a API.

Este comando aceita somente estes dois valores, caso contrário resultará em erro.

## Documentação

- [Visão geral](../README.md "Visão geral")
- [Guia de instalação](INSTALL.md "Guia de instalação")
- [Guia de configuração](CONFIGURATION.md "Guia de configuração")
- [Guia de endpoints](docs/ENDPOINTS.md "Guia de endpoints")
- [Segurança](SECURITY.md)
