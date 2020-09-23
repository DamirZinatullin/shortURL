from wtforms import Form, StringField, TextAreaField

class URLForm(Form):
    long_url = StringField('URL')
    human_readable_text = TextAreaField('human_readable_text')