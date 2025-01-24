import os
from src.config import config_logger

# esconde um dado
def hide_data(data: str) -> str:
    if len(str(data)) >= 4:
        hide = str(data)[0]+'*'*(len(str(data))-2)+str(data)[-1]
    elif len(str(data)) > 0:
        hide = '*'*len(str(data))
    else:
        hide = str(data)
    
    return hide


# limpa o terminal
def clear(info:[str]=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    if info:
        print(info)

    
# altera a cor no terminal
class Colorize:

    def __init__(self, default: str='\033[0m'):
        self.default = default


    def colors(self, color: str) -> str:
        match color:
            case 'y': return '\033[33m' # amarelo
            case 'g': return '\033[32m' # verde
            case 'w': return '\033[37m' # branco
            case 'r': return '\033[31m' # vermelho
            case _: return self.default


    def colorize(self, msg: str, color: str, default: str=None) -> str:
        message = f'{self.colors(color)}{msg}{self.default if not default else self.colors(default)}'
        return message


def wait(env, langs):
    if input(langs(env)[env.LANG]['ENTER_TO_CONTINUE']) == 'exit': clear(); exit()