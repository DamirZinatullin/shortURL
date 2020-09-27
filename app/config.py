import os


class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
        os.getenv('DB_USER', 'flask'),
        os.getenv('DB_PASSWORD', '1'),
        os.getenv('DB_HOST', 'mysql'),
        os.getenv('DB_NAME', 'avito')
    )
