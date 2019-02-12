import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, TextField
from wtforms.validators import DataRequired, ValidationError, InputRequired


class GrowForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[InputRequired()])
    notes = TextField('notes')
    started = HiddenField('started', default=datetime.datetime.utcnow)
    transition = HiddenField('transition')
    ended = HiddenField('ended')
    status = StringField('status', render_kw={'readonly': True})
