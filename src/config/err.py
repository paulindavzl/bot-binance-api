from src.core.lang import langs, c
from src.config.parser import ParserError


def show_error(err: ParserError, env) -> str:
    msg = ''
    match err.name:
        case 'command_error':
            if err.typ == 'command':
                msg = langs(env)[env.LANG]['COMMAND_ERROR'] + err.item
            elif err.typ == 'repeat':
                msg = langs(env)[env.LANG]['COMMAND_ERROR_REPEAT'] + err.item
        
        case 'value_error':
            if err.typ == 'bool':
                msg = langs(env)[env.LANG]['VALUE_ERROR_BOOL'] + err.item

            elif err.typ == 'empty':
                msg = langs(env)[env.LANG]['VALUE_ERROR_EMPTY'] + err.item

            elif err.typ == 'set':
                msg = langs(env)[env.LANG]['VALUE_ERROR_SET']
        
        case 'type_error':
            if err.typ == 'command':
                msg = langs(env)[env.LANG]['TYPE_ERROR'] + err.item
            elif err.typ == 'restart':
                msg = langs(env)[env.LANG]['TYPE_ERROR_RESTART'] + err.item

        case 'sintaxe_error':
            if err.typ == 'command':
                msg = langs(env)[env.LANG]['SINTAXE_ERROR'] + err.item

            elif err.typ == 'invalid':
                msg = langs(env)[env.LANG]['SINTAXE_ERROR_INVALID'] + err.item

            elif err.typ == 'value':
                msg = langs(env)[env.LANG]['SINTAXE_ERROR_VALUE'] + err.item

    
    return msg