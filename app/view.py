from app import app
from models import db
from flask import render_template, request, redirect, url_for, make_response, jsonify, abort
from models import URLModel
from forms import URLForm
import hashids
import traceback
import json


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def create_short_url(url_id: int) -> str:
    hashid = hashids.Hashids(min_length=7)
    short_url = request.host + '/short/' + hashid.encode(url_id)
    return short_url


def add_to_db(url_model: URLModel):
    try:
        db.session.add(url_model)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())


def get_response_from_db(data: json):
    dict_from_data = json.loads(data)
    source_url = dict_from_data.get('source_url', '')
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = URLForm()
        return render_template('index.html', form=form)
    if request.method == 'POST':
        source_url = request.form['source_url']
        data = {"source_url": source_url}
        url_json = get_response_from_db(json.dumps(data))
        return make_response(url_json)


# @app.route('/short-url/api/v1.0/get-short-url/', methods=['GET', 'POST', 'PUT'])
@app.route('/test', methods=['GET'])
def get_short_url():
    if request.method == 'GET':
        json_data = request.get_json()
        return jsonify(json_data)
    else:
        abort(404)
