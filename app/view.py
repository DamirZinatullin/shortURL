from app import app
from models import db
from flask import render_template, request, redirect, url_for, make_response
from models import URLModel
from forms import URLForm
import hashids
import traceback
import json


@app.route('/', methods=['POST', 'GET'])
def index():
    print(request.method)
    if request.method == 'POST':
        long_url = request.form.get('long_url', '')
        try:
            url_model = URLModel.query.filter(URLModel.long_url == long_url).first()
            if url_model:
                pass
            else:
                url_model = URLModel(long_url=long_url)
                db.session.add(url_model)
                db.session.commit()
                url_id = url_model.id
                hashid = hashids.Hashids(min_length=7)
                short_url = request.host + '/short/' + hashid.encode(url_id)
                url_model.short_url = short_url
                db.session.commit()

        except Exception:
            print(traceback.format_exc())
        url_dict = {'source_url': url_model.long_url,
                    'short_url': url_model.short_url}
        return json.dumps(url_dict)

    form = URLForm()
    return render_template('index.html', form=form)


@app.route('/short-url/api/v1.0/<longURL>')
def get_short_url(longURL):
    return longURL
    pass
