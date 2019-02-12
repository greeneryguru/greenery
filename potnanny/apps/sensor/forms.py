from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField
from wtforms.validators import InputRequired, Optional
from potnanny.core.models import Room


class SensorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[InputRequired()])
    model = StringField('model', render_kw={'readonly': True})
    address = StringField('address', render_kw={'readonly': True})
    room_id = SelectField('room assignment', choices=[("", "unassigned")], validators=[Optional()])
