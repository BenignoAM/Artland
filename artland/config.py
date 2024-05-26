class config:
    SECRET_KEY = 'sgfbubiwbcavya'

class DevelopmentConfig(config):
    DEBUG = True
    MYSQL_HOST     = 'localhost'
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB       = 'artland'

config = {
    'development': DevelopmentConfig
}