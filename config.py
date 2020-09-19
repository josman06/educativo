import os

DB_URI = "prueba"

class Config(object):
    SECRET_KEY = '5c063bbb907989439184fce0bf7887074cca1049'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Desarrollo(Config):
    DEBUG = True
    SECRET_KEY = '5c063bbb907989439184fce0bf7887074cca1049'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Kesit023@localhost/prueba'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Produccion(Config):
    DEBUG = False
    host = 'localhost'

