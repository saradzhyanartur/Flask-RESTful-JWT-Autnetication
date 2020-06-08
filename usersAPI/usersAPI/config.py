from datetime import timedelta

#Global Configuration
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

#Redis
class RedisConfig(object):
    HOST = 'localhost'
    PORT = 6379
    DB = 0

#App + Extensions
class InAppConfig(object):
    DEBUG = True
    SERVER_NAME = "127.0.0.1:9000"
    SECRET_KEY = '5b3142dbebffc28cfe6f840d97ea770c74dd7afd' #RESET
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = 'd0f879cd3c50070d0ddfcf99f0d03bb6c1aa3aa4' #RESET
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES