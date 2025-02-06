from src.core.utils import hide_data as hide, clear, Colorize as color


# cria uma instância padrão para Colorize
c = color(color().colors('y')).colorize

def path(env):
    p = fr'({color().colorize("bot-binance-api", 'g')}) {env.BOT_NAME.replace(' ', '_')}:\configure>'
    return p # simula um path

def langs(env):
    languages = {
        # mensagens em português
        'pt': {
            'MSG_DEFAULT_PANEL': f'''Você está realizando a configuração do bot

    Nome do bot: {c(env.BOT_NAME, 'g')}
    Admin. do bot: {c(env.ADM, 'g')}
    GitHub do Admin.: {c(env.GITHUB, 'g')}
    Email: {c(env.EMAIL_ADDRESS, 'g') if env.EMAIL_ADDRESS else c('não configurado', 'r')}
    Certificado TSL: {c('Gerado', 'g') if env.CERTIFICATE else c('Não gerado', 'r')}
    Debug: {c(f'ON - {c('Desative em produção (OFF)', 'r')}' if env.DEBUG else 'OFF', 'g')}
    Status do banco de dados: {c('já configurado', 'g') if env.DB_IS_CONFIGURED else c('não configurado', 'r')}
    Status da API Binance: {c('já configurada', 'g') if env.API_IS_CONFIGURED else c('não configurada', 'r')}
    Tempo de troca de chaves (chave principal/backup):  {c(f'{env.TIME_CHANGE_KEY}/{env.TIME_CHANGE_BACKUP_KEY}', 'g')} (em segundos)
    {c(f'\nPor favor, realize a configuração completa de cada elemento ({c("banco de dados/API Binance", "w", "r")}) para alterar o seus respectivos {c('STATUS', 'w', 'r')}.\nNão é possível iniciar o bot por {c("poetry run app", "w", "r")} ou {c("docker-compose run --service-ports api", "w", "r")} caso o {c("STATUS", "w", "r")} dos elementos não estejam como\n{c("configurado", "g")}\n', 'r') if not all([env.DB_IS_CONFIGURED, env.API_IS_CONFIGURED]) else ''}
    Digite [{c('--help', 'w')}] para ver os comandos ou [{c('exit', 'r')}] para sair

    Type [{c('--lang en', 'w')}] to change the language to English
    ''',

            'ENTER_TO_CONTINUE': f'Aperte {c('ENTER', 'w')} a qualquer momento para continuar\n{path(env)} ',

            'HELP_COMMANDS': f'''Comandos para definir informações do bot ({c('visíveis somente na interface WEB', 'r')}):

        [{c('--name', 'w')}] para definir o nome do bot. Atual: {c(env.BOT_NAME, 'g')}
            ex: {c('--name CryptoSentinel', 'w')}

        [{c('--adm', 'w')}] para definir o administrador do bot. Atual: {c(env.ADM, 'g')}.
            ex: {c('--adm paulindavzl', 'w')}

        [{c('--github', 'w')}] para definir o {c('GitHub', 'w')} do administrador. Atual: {c(env.GITHUB, 'g')}.
            ex: {c('--github https://github.com/paulindavzl', 'w')}

        [{c('--emailaddress', 'w')}] para adicionar um email. Atual: {c(env.EMAIL_ADDRESS, 'g') if env.EMAIL_ADDRESS else c('não configurado', 'r')}.
            ex: {c('--emailaddress my_email@example.com', 'w')}

        [{c('--emailpass', 'w')}] para adicionar a senha do email. Atual: {c(hide(env.EMAIL_PASSWORD), 'g') if env.EMAIL_PASSWORD else c('não configurada', 'r')}.
            ex: {c('--emailpass my_app_password', 'w')}

        [{c('--sendemail', 'w')}] para enviar um email. {c('Disponível', 'g') if all([env.EMAIL_ADDRESS, env.EMAIL_PASSWORD]) else c('Termine a configuração do email.', 'r')}.
            ex: {c('--emailaddress my_email@example.com', 'w')}

        [{c('--certificate', 'w')}] para gerar um certificado TSL, que garante uma comunicação segura entre servidor e cliente.
            ex: {c('--certificate', 'w')}

        [{c('--debug', 'w')}] para alterar o modo de operação do bot (on/off). Atual: {c(env.GITHUB, 'g')}.
            ex: {c('--debug on/off', 'w')} {c(f'Usar valores diferente de {c("on/off", "w", "r")} resultará no valor padrão ({c("on", "w", "r")})', 'r')}

    Comandos para definir configurações do banco de dados ({c('já configurado', 'g') if env.DB_IS_CONFIGURED else c('não configurado', 'r')}):
        
        [{c('--user', 'w')}] para definir o usuário. Atual: {c(env.DB_USER, 'g' if env.DB_USER != 'Null' else 'r')}
            ex: {c('--user root', 'w')}

        [{c('--host', 'w')}] para definir o servidor. Atual: {c(env.DB_HOST, 'g' if env.DB_HOST != 'Null' else 'r')}
            ex: {c('--host localhost', 'w')}

        [{c('--port', 'w')}] para definir a porta. Atual: {c(env.DB_PORT, 'g' if env.DB_PORT != 'Null' else 'r')}
            ex: {c('--port 3306', 'w')}

        [{c('--pass', 'w')}] para definir a senha. Atual: {c(hide(env.DB_PASSWORD), 'g') if env.DB_PASSWORD != 'Null' else c('Null', 'r')}
            ex: {c('--pass my_password_123', 'w')}

        [{c('--dbname', 'w')}] para definir o usuário. Atual: {c(env.DB_NAME, 'g' if env.DB_NAME != 'Null' else 'r')}
            ex: {c('--dbname database', 'w')}

    Comandos para definir configurações da API Binance ({c('já configurado', 'g') if env.API_IS_CONFIGURED else c('não configurado', 'r')}):

        [{c('--accesskey', 'w')}] para definir a chave de acesso. Atual: {c(hide(env.ACCESS_KEY), 'g') if env.ACCESS_KEY != 'Null' else c('Null', 'r')}
            ex: {c('--accesskey my_access_key_123', 'w')}
        
        [{c('--secretkey', 'w')}] para definir a chave secreta. Atual: {c(hide(env.SECRET_KEY), 'g') if env.SECRET_KEY != 'Null' else c('Null', 'r')}
            ex: {c('--secretkey my_secret_key_123', 'w')}

    Comandos para alterar o tempo de trocas das chaves de decodificação:

        [{c('--timekey', 'w')}] para definir o tempo de troca da chave principal ({c('em segundos', 'w')}). Atual: {c(env.TIME_CHANGE_KEY, 'g')}
            ex: {c('--timeket 3600', 'w')}

        [{c('--timebackup', 'w')}] para definir o tempo de troca da chave de backup ({c('em segundos', 'w')}). Atual: {c(env.TIME_CHANGE_BACKUP_KEY, 'g')}
            ex: {c('--timebackup 600', 'w')}

    Reiniciar as configurações do bot para o padrão ({c('não recomendado e irreversível', 'r')}):

        [{c('--restart_system', 'w')}] reiniciará todas as configurações para o padrão{c('permanentemente', 'r')}.
            ex: {c('--restart_system', 'w')}

    Outros comandos:

        [{c('--lang en', 'w')}] to change the language to English

        [{c('-y', 'w')}] para {c('confirmar', 'g')} todas as mudanças automaticamente ({c('somente no final do comando', 'r')})
            ex: {c('--secretkey my_secret_key_123 --y', 'w')}

        [{c('-n', 'w')}] para {c('negar', 'r')} todas as mudanças automaticamente ({c('somente no final do comando', 'r')})
            ex: {c('--secretkey my_secret_key_123 --n', 'w')}

        [{c('--set api/dbs', 'w')}] para definir cada elemento configurado.

    Nota: 
        Para usar espaços em branco ou caractéres especiais, use aspas simples ou duplas:
            exs: 
                {c('--pass my password 123', 'r')}
                {c('--pass "my password 123"', 'g')}

        Você pode usar vários comandos de uma vez:
            ex: {c('--user root --host localhost --port 3306 --pass my_password --dbname database --y', 'w')}
    ''',

            'COMMAND_ERROR': 'CommandError: Este comando não exite. Comando: ',

            'COMMAND_ERROR_REPEAT': 'CommandError: Não é permitido repetir comandos na mesma linha. Comando: ',

            'VALUE_ERROR_BOOL': 'ValueError: Este comando não aceita nenhum tipo de valor. Comando: ',

            'VALUE_ERROR_EMPTY': 'ValueError: Este comando exige um valor e não pode estar vazio. Comando: ',

            'VALUE_ERROR_SET': 'ValueError: O comando set aceita somente api/dbs como valor',

            'TYPE_ERROR': 'TypeError: Estes comandos não podem ser usados juntos. Comandos: ',

            'TYPE_ERROR_RESTART': 'TypeError: O comando --restart_system não pode ser usado com outros comandos (exceto -y / -n). Comando: ',

            'SINTAXE_ERROR': 'SintaxeError: O comando possui caractére inválido. Comando: ',

            'SINTAXE_ERROR_INVALID': 'SintaxeError: O comando pode estar escrito de forma errada ou não existe. Comando: ',

            'SINTAXE_ERROR_VALUE': 'SintaxeError: O valor deste comando possui caractéres inválidos. Comando: ',

            'ALL_CANCELED': 'Todos o comandos foram cancelado por conta da presença de "-n".',

            'EXECUTE_COMMAND': f'Deseja executar este comando? [{c("y", "g", "w")}/{c("n", "r", "w")}]. Comando: ',

            'INVALID_RESPONSE': 'Sua resposta não é válida. Escolha entre as seguintes: ',

            'RESTART_SYSTEM_CONFIRM': f'Confirme que você quer reiniciar todo o sistema para configuração inicial.\nIsso apagará todos os arquivos contidos em {c('logs/', 'w', 'r')}, os arquivos {c('.env', 'w', 'r')}, {c('.enc', 'w', 'r')} e {c('.key', 'w', 'r')} também serão apagados!',

            'RESTART_SYSTEM_SUCCESSFULLY': f'Todo o sistema foi restaurado para a configuração inicial.\nNote que informações contidas em {c('bancos de dados', 'w', 'g')} continuam inalteradas!\nAltere manualmente se necessário.',

            'EMAIL_NOT_CONFIGURED': f'{c('A configuração do email está incompleta.', 'r')} {c('Use --emailaddress para adicionar um email e --emailpass para adicionar a senha', 'w')}',

            'SET_SUBJECT': c('Informe o assunto deste email: ', 'y', 'w'),

            'SET_CONTENT': c('Informe o contúdo do email: ', 'y', 'w'),

            'INVALID_CREDENTIALS': c('Os dados de endereço de e-mail ou senha estão incorretos! Não foi possível enviar o email.', 'r'),

            'SUCCESSFULLY_EMAIL_SEND': c(f'O e-mail foi enviado com sucesso! {c('Verifique a Caixa de Entrada ou Spam', 'w')}', 'g'),

            'CERTIFICATE_EXISTS': c('O certificado já existe!', 'r'),

            'CERTIFICATE_INCOMPLETE': f'{c('O certificado existe, mas está incompleto!', 'r')} {c('Você deseja gerá-lo novamente?', 'w', 'w')} [{c("y", "g", "w")}/{c("n", "r", "w")}]',

            'OPENSSL_UNINSTALED': f'{c('Parece que o OpenSSL não está instalado no seu sistema!', 'r')} {c('Talvez você esteja executando a API fora do contêiner Docker. Se for caso, instale o OpenSSL.', 'w')}',

            'CERTIFICATE_GENERATED': c('O certificado TSL foi gerado com sucesso!', 'g'),

            'CERTIFICATE_GENERATED_FAILED': c('Houve um erro ao gerar o certificado!', 'r')
        },

        # mensagens em inglês
        'en': {
            'MSG_DEFAULT_PANEL': f'''You are configuring the bot

    Bot name: {c(env.BOT_NAME, 'g')}
    Admin. from bot: {c(env.ADM, 'g')}
    Admin GitHub: {c(env.GITHUB, 'g')}
    Email: {c(env.EMAIL_ADDRESS, 'g') if env.EMAIL_ADDRESS else c('not configured', 'r')}
    TSL Certificate: {c('Generated', 'g') if env.CERTIFICATE else c('Not generated', 'r')}
    Debug: {c(f'ON - {c('Disable in production (OFF)', 'r')}' if env.DEBUG else 'OFF', 'g')}
    Database status: {c('already configured', 'g') if env.DB_IS_CONFIGURED else c('not configured', 'r')}
    Binance API Status: {c('already configured', 'g') if env.API_IS_CONFIGURED else c('not configured', 'r')}
    Key exchange time (main/backup key): {c(f'{env.TIME_CHANGE_KEY}/{env.TIME_CHANGE_BACKUP_KEY}', 'g')} (in seconds)
    {c(f'\nPlease perform full configuration of each element ({c("Binance database/API", "w", "r")}) to change their respective {c('STATUS', 'w', 'r')}.\nCannot start the bot by {c("poetry run app", "w", "r")} or {c("docker-compose run --service-ports api", "w", "r")} if the {c("STATUS", "w", "r")} of the elements are not as\n{c("configured", "g")}\n', 'r') if not all([env.DB_IS_CONFIGURED, env.API_IS_CONFIGURED]) else ''}

    Type [{c('--help', 'w')}] to see the commands or [{c('exit', 'r')}] to exit

    Digite [{c('--lang pt', 'w')}] para alterar o idioma para Português
    ''',

            'ENTER_TO_CONTINUE': f'Press {c('ENTER', 'w')} at any time to continue\n{path(env)} ',

            'HELP_COMMANDS': f'''Commands to define bot information ({c('visible only in the WEB interface', 'r')}):

        [{c('--name', 'w')}] to set the bot name. Current: {c(env.BOT_NAME, 'g')}
            ex: {c('--name CryptoSentinel', 'w')}

        [{c('--adm', 'w')}] to set the bot administrator. Current: {c(env.ADM, 'g')}.
            ex: {c('--adm paulindavzl', 'w')}

        [{c('--github', 'w')}] to set the admin's {c('GitHub', 'w')}. Current: {c(env.GITHUB, 'g')}.
            ex: {c('--github https://github.com/paulindavzl', 'w')}

        [{c('--emailaddress', 'w')}] to add an email. Current: {c(env.EMAIL_ADDRESS, 'g') if env.EMAIL_ADDRESS else c('not configured', 'r')}.
            ex: {c('--emailaddress my_email@example.com', 'w')}

        [{c('--emailpass', 'w')}] to add the email password. Current: {c(hide(env.EMAIL_PASSWORD), 'g') if env.EMAIL_PASSWORD else c('not configured', 'r')}.
            ex: {c('--emailpass my_app_password', 'w')}

        [{c('--sendemail', 'w')}] to send an email. {c('Available', 'g') if all([env.EMAIL_ADDRESS, env.EMAIL_PASSWORD]) else c('Finish email configuration.', 'r')}.
            ex: {c('--emailaddress my_email@example.com', 'w')}

        [{c('--certificate', 'w')}] to generate a TSL certificate, which guarantees secure communication between server and client.
            ex: {c('--certificate', 'w')}

        [{c('--debug', 'w')}] to change the bot's operating mode (on/off). Current: {c(env.GITHUB, 'g')}.
            ex: {c('--debug on/off', 'w')} {c(f'Using values ​​other than {c("on/off", "w", "r")} will result in the default value ({c("on", "w", "r")})', 'r')}

    Commands to configure database settings ({c('already configured', 'g') if env.DB_IS_CONFIGURED else c('not configured', 'r')}):
        
        [{c('--user', 'w')}] to define the user. Current: {c(env.DB_USER, 'g' if env.DB_USER != 'Null' else 'r')}
            ex: {c('--user root', 'w')}

        [{c('--host', 'w')}] to define the server. Current: {c(env.DB_HOST, 'g' if env.DB_HOST != 'Null' else 'r')}
            ex: {c('--host localhost', 'w')}

        [{c('--port', 'w')}] to set the port. Current: {c(env.DB_PORT, 'g' if env.DB_PORT != 'Null' else 'r')}
            ex: {c('--port 3306', 'w')}

        [{c('--pass', 'w')}] to set the password. Current: {c(hide(env.DB_PASSWORD), 'g') if env.DB_PASSWORD != 'Null' else c('Null', 'r')}
            ex: {c('--pass my_password_123', 'w')}

        [{c('--dbname', 'w')}] to define the user. Current: {c(env.DB_NAME, 'g' if env.DB_NAME != 'Null' else 'r')}
            ex: {c('--dbname database', 'w')}

    Commands to configure Binance API settings ({c('already configured', 'g') if env.API_IS_CONFIGURED else c('not configured', 'r')}):

        [{c('--accesskey', 'w')}] to set the access key. Current: {c(hide(env.ACCESS_KEY), 'g') if env.ACCESS_KEY != 'Null' else c('Null', 'r')}
            ex: {c('--accesskey my_access_key_123', 'w')}
        
        [{c('--secretkey', 'w')}] to set the secret key. Current: {c(hide(env.SECRET_KEY), 'g') if env.SECRET_KEY != 'Null' else c('Null', 'r')}
            ex: {c('--secretkey my_secret_key_123', 'w')}

    Commands to change the decryption key exchange time:

        [{c('--timekey', 'w')}] to set the main key exchange time ({c('in seconds', 'w')}). Current: {c(env.TIME_CHANGE_KEY, 'g')}
            ex: {c('--timeket 3600', 'w')}

        [{c('--timebackup', 'w')}] to set the backup key exchange time ({c('in seconds', 'w')}). Current: {c(env.TIME_CHANGE_BACKUP_KEY, 'g')}
            ex: {c('--timebackup 600', 'w')}

    Reset bot settings to default ({c('not recommended and irreversible', 'r')}):

        [{c('--restart_system', 'w')}] will reset all settings to default {c('permanently', 'r')}.
            ex: {c('--restart_system', 'w')}

    Other commands:

        [{c('--lang pt', 'w')}] para mudar o idioma para Português

        [{c('-y', 'w')}] to {c('commit', 'g')} all changes automatically ({c('only at end of command', 'r')})
            ex: {c('--secretkey my_secret_key_123 --y', 'w')}

        [{c('-n', 'w')}] to {c('negate', 'r')} all changes automatically ({c('only at end of command', 'r')})
            ex: {c('--secretkey my_secret_key_123 --n', 'w')}

        [{c('--set api/dbs', 'w')}] to set each configured element.

    Note: 
        To use whitespace or special characters, use single or double quotes:
            ex: 
                {c('--pass my password 123', 'r')}
                {c('--pass "my password 123"', 'g')}

        You can use multiple commands at once:
            ex: {c('--user root --host localhost --port 3306 --pass my_password --dbname database --y', 'w')}
    ''',

            'COMMAND_ERROR': 'CommandError: This command does not exist. Command: ',

            'COMMAND_ERROR_REPEAT': 'CommandError: Repeating commands on the same line is not allowed. Command: ',

            'VALUE_ERROR_BOOL': 'ValueError: This command does not accept any value type. Command: ',

            'VALUE_ERROR_EMPTY': 'ValueError: This command requires a value and cannot be empty. Command: ',

            'VALUE_ERROR_SET': 'ValueError: Set command accepts only api/dbs as value',

            'TYPE_ERROR': 'TypeError: These commands cannot be used together. Commands: ',

            'TYPE_ERROR_RESTART': 'TypeError: The --restart_system command cannot be used with other commands (except -y / -n). Command: ',

            'SINTAXE_ERROR': 'SyntaxError: The command has an invalid character. Command: ',
            
            'SINTAXE_ERROR_INVALID': 'SintaxeError: The command may be written wrong or does not exist. Command: ',

            'SINTAXE_ERROR_VALUE': 'SyntaxError: The value of this command has invalid characters. Command: ',

            'ALL_CANCELED': 'All commands were canceled due to the presence of "-n".',

            'EXECUTE_COMMAND': f'Do you want to execute this command? [{c("y", "g", "w")}/{c("n", "r", "w")}]. Command: ',

            'INVALID_RESPONSE': 'Your response is not valid. Choose from the following: ',

            'RESTART_SYSTEM_CONFIRM': f'Confirm that you want to reset the entire system to initial configuration.\nThis will delete all files contained in {c('logs/', 'w')}, the files {c('.env', 'w')}, {c('.enc', 'w')} and {c('.key', 'w')} will also be deleted!',

            'EMAIL_NOT_CONFIGURED': f'{c('Email configuration is incomplete.', 'r')} {c('Use --emailaddress to add an email and --emailpass to add a password', 'w') }',

            'SET_SUBJECT': c('Enter the subject of this email: ', 'y', 'w'),

            'SET_CONTENT': c('Enter the content of the email: ', 'y', 'w'),

            'INVALID_CREDENTIALS': c('Email address or password data is incorrect! Email could not be sent.', 'r'),

            'SUCCESSFULLY_EMAIL_SEND': c(f'The email was sent successfully! {c('Check your Inbox or Spam', 'w')}', 'g')
        }
    }

    return languages