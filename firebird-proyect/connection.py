from firebird.driver import connect, driver_config

def create_connection_db():
    #Ubicacion del servidor de FireBird
    driver_config.server_defaults.host.value = 'localhost'

    #Usuario FireBird
    driver_config.server_defaults.user.value = 'sysdba'

    #Clave FireBird
    driver_config.server_defaults.password.value = 'masterkey'
    
    #PC1
    connection = connect('C:\\Users\\PC\\Downloads\\TP1-TipoA-20240714T133652Z-001\\TP1-TipoA\\MAXDETALLESPORFACTURA.FDB')
    
    #PC2
    #connection = connect('C:\\Users\\Santi\\Documents\\DBd-FlameRobin\\MAXDETALLESPORFACTURA.FDB')

    return connection