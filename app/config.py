import os


class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.getenv('DB_USER', 'flask'),
        os.getenv('DB_PASSWORD', '1'),
        os.getenv('DB_HOST', 'mysql'),
        os.getenv('DB_NAME', 'avito')
    )
