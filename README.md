# CryptoSentinel

CryptoSentinel é uma API e bot desenvolvido para conectar-se à [Binance](https://binance.com/) e realizar operações automatizadas em criptomoedas. Ele foi projetado para ser seguro, flexível e fácil de configurar, mesmo para iniciantes.

## Dependências

<a href="https://www.docker.com/" target="_blank"><img src="https://github.com/user-attachments/assets/94c615fb-79d1-46b3-848e-667f9e312716" alt="Docker" width="130" height="130" title="usa Docker para manter a consistência do projeto em todas as máquinas"></a>
<a href="https://python-poetry.org/docs/" target="_blank"><img src="https://github.com/user-attachments/assets/5be6ef37-662a-4319-8a7f-f0ed1b15ba37" alt="Poetry" width="130" height="130" title="usa Poetry para gerenciar dependências"></a>
<a href="https://flask.palletsprojects.com/en/stable/installation/" target="_blank"><img src="https://github.com/user-attachments/assets/034ef091-fb20-4193-8945-71dd748b053c" alt="Flask" width="130" height="130" title="usa Flask para criar a API"></a>
<a href="https://www.mysql.com/downloads/" target="_blank"><img src="https://github.com/user-attachments/assets/629d1c03-6807-48d5-9fa5-6e12b3446e1e" alt="MySQL" width="130" height="130" title="usa MySQL como SGDB"></a>

O **Flask** é uma dependência que é instalada automaticamente, mas caso você não tenha o **Poetry**, **Docker** ou **MySQL** (caso execute localmente), veja como instalá-los clicando em seus logos acima.

## Funcionalidades

Esta API/bot conta com diversas funcionalidades que facilitam sua implementação, manuntenção e personalização:

### Prompt próprio

A API tem um prompt de comandos que facilita a sua configuração, com o usuário podendo definir o Banco de Dados (MySQL) e a chaves de API para conexão com a Binance:

![Prompt de configuração](docs/img/prompt-configuration.png "Prompt de comando")

O prompt possui uma versão em `português` e `inglês`. Veja [comandos](docs/COMMANDS.md).

### Facilidade de personalização

Por meio do prompt de configuração é possível personalizar informações do bot, estas são acessadas por [endpoints](docs/ENDPOINTS.md) e ficam visíveis na interface WEB (em desenvolvimento). Veja [comandos](docs/COMMANDS.md).

### Segurança

As chaves de APIs, informações dos banco de dados e outras informações ficam salvas em variáveis de ambiente criptografadas.

![segurança](docs/img/security-image.png)

O usuário pode definir um mecanismo para proteger as chaves (AWS) modificando duas funções em:

![mecanismo de chaves](docs/img/key-mechanism.png)

Veja [segurança](docs/SECURITY.md)

## Documentação

- [Guia de instalação](docs/INSTALL.md)
- [Guia de comandos](docs/COMMANDS.md)
- [Guia de configuração](docs/CONFIGURATION.md)
- [Guia de endpoints](docs/ENDPOINTS.md)
- [Segurança](docs/SECURITY.md)
