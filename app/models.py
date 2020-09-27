from app import app
from app import db
import sqlalchemy


import time


def create_tables(db):
    db.create_all()


class URLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(2048))
    short_url = db.Column(db.String(100))
    human_readable_url = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(URLModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<URL id:{self.id}, short_URL: {self.short_url}, slug_URL:{self.slug_url}>'


while True:
    try:
        create_tables(db=db)
        break
    except sqlalchemy.exc.OperationalError:
        print('The database server is still unavailable')
        time.sleep(10)
