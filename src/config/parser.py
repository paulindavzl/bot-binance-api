import re
import string

class ParserError:
    def __init__(self, name: str, item, typ: str='command'):
        self.name=name
        self.item=item
        self.typ = typ

    
    def __str__(self):
        return f'{self.name}, {self.item}, {self.typ}'


class Parser:
    def __init__(self, cmd: str):
        self._cmd = cmd
        self._valid_commands = ['--lang', '--user', '--host', '--port', '--pass', '--dbname', '--name', '--github', '--adm', '--accesskey', '--secretkey', '--timekey', '--timebackup', '--restart_system', '-y', '-n']
        self._unique_cmd = 0
        self._cmd_used = []
        self._cmd_bools = ['-y', '-n', '--restart_system'] # comandos que exigem valores booleanos
        self._commands = {'-y': False, '-n': False} # garda os comandos e seus valores
        self._err = False
        self._parser()

    
    # retorna o resultado
    @property
    def result(self) -> dict:
        return self._commands

    
    # separa os comandos e valores
    def _parser(self):
        # separa o padrão para comandos e valores
        pattern = re.compile(r'(?P<command>(?! )--?\w+|-- ?\w+|---\w+)\s*(?P<value>(?!-)["\'].+["\']|(?!-)\S+)?')
        matchers = pattern.finditer(self._cmd)

        for match in matchers:
            # separa comandos e valores
            command = match.group('command')
            value = match.group('value')

            # verifica se não possui erro
            self._validate(command, value)
            if not self._err:
                # adiciona os comandos e valores no dicionário
                self._commands[command] = value.strip('"\'') if value else True

    
    # agrupa as verificações de erros
    def _validate(self, cmd, value):
        permitted_chars = set(string.ascii_letters + string.digits + '-_.@/:')

        self._validate_sintaxe(cmd, value, permitted_chars)
        if not self._err:
            self._validate_command(cmd, value)

        if not self._err:
            if '--restart_system' in self._cmd_used:
                for c in self._cmd_used:
                    if not c in self._cmd_bools:
                        self._commands = {'err': ParserError('type_error', c, 'restart')}
                        self._err = True

    
    # valida o comando e o valor atribuído à ele
    def _validate_command(self, cmd, value):
        if cmd in self._cmd_bools[:2]:
            self._unique_cmd += 1

        # garante que o comando é válido
        if not cmd in self._valid_commands:
            self._commands = {'err': ParserError('command_error', cmd)}
            self._err = True

        elif cmd in self._cmd_used:
            self._commands = {'err': ParserError('command_error', cmd, 'repeat')}
            self._err = True

        elif cmd in self._cmd_bools and not (isinstance(value, bool) or value is None):
            self._commands = {'err': ParserError('value_error', cmd, 'bool')}
            self._err = True

        elif not cmd in self._cmd_bools and not isinstance(value, str):
            self._commands = {'err': ParserError('value_error', cmd, 'empty')}
            self._err = True

        elif self._unique_cmd > 1:
            self._commands = {'err': ParserError('type_error', '-y & -n')}
            self._err = True

        self._cmd_used.append(cmd)
        
    
    # valida a sintaxe
    def _validate_sintaxe(self, cmd, value, permitted_chars: list):
        # verifica se o comando inicia com -- ou -
        if not cmd.startswith('--'):
            if not len(cmd) == 2 or not cmd.startswith('-'):
                self._commands = {'err': ParserError('sintaxe_error', cmd, 'invalid')}
                self._err = True

        # verfica se o comando possui somente caractéres permitidos
        elif not set(cmd).issubset(permitted_chars):
            self._commands = {'err': ParserError('sintaxe_error', cmd)}
            self._err = True

        # verifica se o valor possui somente caractéres permitidos
        if isinstance(value, str) and not ((value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))) and not set(value).issubset(permitted_chars):
            self._commands = {'err': ParserError('sintaxe_error', cmd, 'value')}
            self._err = True
