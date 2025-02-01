import string
from src.config import config_logger
from src.config import restart_system
from src.core.lang import langs, c, clear, path
from src.core.utils import wait


class Execute:
    def __init__(self, cmd: dict, env, response: str):
        self._commands = cmd
        self._executed = None
        self._env = env
        self._tranlasted_commands = []
        self._response = response
        self._y = False
        self._n = False
        self._translation = {'--name': 'BOT_NAME', '--adm': 'ADM', '--github': 'GITHUB', '--lang': 'LANG', '--debug': 'DEBUG', '--user': 'DB_USER', '--host': 'DB_HOST', '--port': 'DB_PORT', '--pass': 'DB_PASSWORD', '--dbname': 'DB_NAME', '--accesskey': 'ACCESS_KEY', '--secretkey': 'SECRET_KEY', '--timekey': 'TIME_CHANGE_KEY', '--timebackup': 'TIME_CHANGE_BACKUP_KEY'}
        self._translate()
        self._execute()


    # retorna os comandos executados
    @property
    def executed(self) -> list:
        return self._executed

    
    # traduz os comandos
    def _translate(self):
        self._y = self._commands.pop('-y')
        self._n = self._commands.pop('-n')
        self._restart_system = self._commands.pop('--restart_system') if self._commands.get('--restart_system') else False

        for cmd in self._commands:
            if cmd != '--set':
                self._tranlasted_commands.append([cmd, self._translation[cmd]])
            else:
                self._tranlasted_commands.append([cmd, 'API_IS_CONFIGURED' if self._commands[cmd] == 'api' else 'DB_IS_CONFIGURED'])

    
    # executa os comandos
    def _execute(self):
        permitted_chars = set(string.ascii_letters + string.digits + '-_.@/:')

        if self._restart_system:
            restart_system.run(self._env, self._y, self._n)
            self._env.load_file_env(True)
            # garante que _executed seja uma lista
            if not self._executed:
                self._executed = []

            self._executed.append('--restart_system')

            return

        for command in self._tranlasted_commands:
            if self._n:
                clear(f"{path(self._env)} {self._response}\n{c(langs(self._env)[self._env.LANG]['ALL_CANCELED'], 'r')}")
                wait(self._env, langs)
                return
        
            resp = True
            while resp:
                vl = self._commands[command[0]]
                msg = langs(self._env)[self._env.LANG]['EXECUTE_COMMAND'] + f'{command[0]} {vl if set(vl).issubset(permitted_chars) else f"{vl}"}'
                clear(c(msg, "w"))

                if command[1] == 'DEBUG':
                    if vl.lower() == 'on':
                        vl = True
                    elif vl.lower() == 'off':
                        vl = False
                    else:
                        vl = True

                if command[0] == '--set':
                    vl = True

                response = 'y'
                if not self._y:
                    response = input(f'{path(self._env)}(n) ')
                else:
                    config_logger().warning('All commands were authorized by -y')

                if response == 'y':
                    if command[1] == 'LANG':
                        if vl not in ['pt', 'en']:
                            vl = 'pt'

                    kwarg_cmd = {command[1]:vl}
                    self._env.set_env(reload=True, **kwarg_cmd)

                    if command[0] == '--debug':
                        if vl: vl = 'on'
                        else: vl = 'off'

                    elif command[0] == '--set':
                        vl = 'api' if command[1] == 'API_IS_CONFIGURED' else 'dbs'

                    # garante que _executed seja uma lista
                    if not self._executed:
                        self._executed = []

                    self._executed.append(command[0])

                    clear(f"\n{path(self._env) + response}\n{c('Executado:' if self._env.LANG == 'pt' else 'Executed:', 'g')} {c(f'{command[0]} {vl if set(vl).issubset(permitted_chars) else f"{vl}"}', 'w')}\n")
            
                    resp = False
                    wait(self._env, langs)

                elif response == 'n' or len(response) == 0:
                    config_logger().info(f'The command {command[0]} was denied')
                    response = 'n'
                    clear(f"\n\n{path(self._env) + response}\n{c('Cancelado:' if self._env.LANG == 'pt' else 'Canceled:', 'r')} {c(f'{command[0]} {vl if set(str(vl)).issubset(permitted_chars) else f"{vl}"}', 'w')}\n\n")
                    resp = False
                    wait(self._env, langs)

                else:
                    config_logger().info(f'Invalid response: {response}')
                    clear(f"{path(self._env) + response}\n{c(langs(self._env)[self._env.LANG]['INVALID_RESPONSE'], 'r', 'w')} [y / n]")
                    wait(self._env, langs)