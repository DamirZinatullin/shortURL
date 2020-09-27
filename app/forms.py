from wtforms import Form, StringField, TextAreaField
from wtforms.validators import URL, InputRequired


class URLForm(Form):
    source_url = StringField(id='source_url', validators=[URL()])
    human_readable = StringField('human_readable')
