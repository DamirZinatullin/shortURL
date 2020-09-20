from flask import Flask, Response
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
db.create_all()


@app.route('/')
def index() -> str:
    resp = Response("Hello world", status=200)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
