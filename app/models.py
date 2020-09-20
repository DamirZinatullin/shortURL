from app import db


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(2048))
    short_url = db.Column(db.String(30))
    slug_url = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(URL, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<URL id:{self.id}, short_URL: {self.short_url}, slug_URL:{self.slug_url}>'