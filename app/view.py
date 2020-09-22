from app import app
from models import db
from flask import render_template, request, redirect, url_for, make_response
from models import URL

@app.route('/')
def index() -> str:
    resp = "Hello world"
    return resp