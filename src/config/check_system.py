import src.__init__ as env

# verifica se as informações importantes estão configuradas
def is_ok():
    if all([env.API_IS_CONFIGURED, env.DB_IS_CONFIGURED]):
        return True
    return False