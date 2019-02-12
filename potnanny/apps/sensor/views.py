from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_jwt_extended import jwt_required

from potnanny.extensions import db
from .forms import SensorForm
from potnanny.core.schemas import SensorSchema
from potnanny.core.models import Sensor, Room
from potnanny.crud import CrudInterface



bp = Blueprint('sensor', __name__,
                    template_folder='templates', url_prefix='/sensors')
ifc = CrudInterface(Sensor, SensorSchema)


@bp.route('/', methods=['GET'])
@jwt_required
def index():
    data = []
    sensors = Sensor.query.all()
    for s in sensors:
        obj = {
            'id': s.id,
            'name': s.name,
            'address': s.address,
            'model': s.model,
            'room': 'unassigned',
        }
        if s.room:
            obj['room'] = s.room

        data.append(obj)

    return render_template('sensor/index.html',
                title='Sensors',
                payload=data)


@bp.route('/<int:pk>/measurements', methods=['GET'])
@jwt_required
def get_measurements(pk):
    serialized, results, code = ifc.get(pk, ['measurements', 'latest_readings'])
    if not serialized:
        return None

    return jsonify(serialized)


@bp.route('/<pk>/edit', methods=['GET','POST'])
@jwt_required
def edit(pk):
    title = 'Edit Sensor'
    sensor = Sensor.query.get_or_404(pk)

    form = SensorForm(obj=sensor)

    rooms = Room.query.all()
    for r in rooms:
        form.room_id.choices.append((str(r.id), r.name))

    if request.method == 'POST' and form.validate_on_submit():
        sensor.name = form.name.data
        if form.room_id.data and form.room_id.data != "":
            room = Room.query.get(int(form.room_id.data))
            sensor.room = room

        db.session.commit()

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/sensors')

    return render_template('sensor/form.html',
        form=form,
        title=title)
