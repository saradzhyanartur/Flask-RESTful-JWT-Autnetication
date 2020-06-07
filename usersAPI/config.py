class Config(object):
    DEBUG = True
    SERVER_NAME = "127.0.0.1:5000"
    SECRET_KEY = '5b3142dbebffc28cfe6f840d97ea770c74dd7afd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = False
    JWT_SECRET_KEY = 'd0f879cd3c50070d0ddfcf99f0d03bb6c1aa3aa4'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']