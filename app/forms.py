from wtforms import Form, StringField, TextAreaField


class URLForm(Form):
    long_url = StringField(id='long_url')
    human_readable = StringField('human_readable')
