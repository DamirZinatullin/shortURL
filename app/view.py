from app import app
from models import db
from flask import render_template, request, redirect, url_for, make_response, jsonify, abort
from models import URLModel
from forms import URLForm
import hashids
import traceback
import re
from sqlalchemy import or_


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def create_short_url(url_id: int) -> str:
    hashid = hashids.Hashids(min_length=7)
    short_url = 'http://0.0.0.0:8000' + '/short-url/' + hashid.encode(url_id)
    return short_url


def create_human_readable_url(human_readable: str) -> str:
    human_readable_url = r'http://0.0.0.0:8000' + r'/short-url/' + slugify(human_readable)
    return human_readable_url


def add_to_db(url_model: URLModel):
    try:
        db.session.add(url_model)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())


def get_response_for_short_url(request_data: dict):
    source_url = request_data.get('source_url', '')
    if source_url:
        url_model = URLModel.query.filter(URLModel.source_url == source_url).first()
        if not url_model:
            url_model = URLModel(source_url=source_url)
            add_to_db(url_model)
            short_url = create_short_url(url_model.id)
            url_model.short_url = short_url
            db.session.commit()
        url_dict = {'source_url': url_model.source_url,
                    'short_url': url_model.short_url}
        return jsonify(url_dict)
    else:
        return make_response('Wrong request')


def get_response_for_readable_url(request_data: dict):
    source_url = request_data.get('source_url', '')
    human_readable = request_data.get('human_readable', '')
    if source_url and human_readable:
        url_model = URLModel.query.filter(URLModel.source_url == source_url).first()
        human_readable_url = create_human_readable_url(human_readable)
        if not url_model:
            url_model = URLModel(source_url=source_url, human_readable_url=human_readable_url)
            add_to_db(url_model)
            short_url = create_short_url(url_model.id)
            url_model.short_url = short_url
            db.session.commit()
        else:
            url_model.human_readable_url = human_readable_url
            db.session.commit()
        url_dict = {'source_url': url_model.source_url,
                    'short_url': url_model.short_url,
                    'human_readable_url': url_model.human_readable_url}
        return jsonify(url_dict)
    else:
        return make_response('Wrong request')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = URLForm()
        return render_template('index.html', form=form)
    if request.method == 'POST':
        source_url = request.form['source_url']
        human_readable = request.form['human_readable']
        data = {"source_url": source_url, 'human_readable': human_readable}
        if human_readable:
            return get_response_for_readable_url(data)
        else:
            return get_response_for_short_url(data)


@app.route('/short-url/api/v1.0/get-short-url/', methods=['POST', 'GET', 'PUT'])
def get_short_url():
    request_data = request.get_json()
    source_url = request_data.get('source_url', '')
    human_readable = request_data.get('human_readable', '')
    url_form = URLForm(source_url=source_url, human_readable=human_readable)
    if url_form.validate():
        if human_readable:
            return get_response_for_readable_url(request_data)
        else:
            return get_response_for_short_url(request_data)
    else:
        abort(404)


@app.route('/short-url/<short_url>', methods=['GET'])
def redirect_to_source(short_url):
    url_model = URLModel.query.filter(or_(
        URLModel.short_url == request.url, URLModel.human_readable_url == request.url)).first()
    if url_model:
        return redirect(url_model.source_url)
    else:
        abort(404)
