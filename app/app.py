from flask import Flask, Response
from config import Configuration
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)







