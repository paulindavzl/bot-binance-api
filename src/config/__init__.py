import json

PATH_CONFIG = 'src/config'

@property
def DEFAULT_CONFIG_JSON() -> object:
    config = {
        'is_configured': 0
    }

    default_config = json.dumps(config, indent=4)

    return default_config