from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_jwt_extended import jwt_required

from potnanny.core.models import Room, Sensor
from potnanny.crud import CrudInterface
from potnanny.core.schemas import RoomSchema, SensorSchema
from potnanny.extensions import db
from .forms import RoomForm

bp = Blueprint('room', __name__,
                    template_folder='templates', url_prefix='/rooms')
ifc = CrudInterface(Room, RoomSchema)

@bp.route('/', methods=['GET'])
@jwt_required
def index():
    serialized, err, code = ifc.get()
    if err:
        pass

    return render_template('room/index.html',
                title='Rooms',
                payload=serialized)


@bp.route('/<int:pk>', methods=['GET'])
@jwt_required
def get(pk):
    serialized, err, code = ifc.get(pk, ['environment', 'environment'])
    if err:
        pass

    return jsonify(serialized)


@bp.route('/<int:pk>/sensors', methods=['GET'])
@jwt_required
def get_room_sensors(pk):
    data = []
    sfc = CrudBase(Sensor, SensorSchema)
    r = Room.query.get(pk)
    if r:
        for s in r.sensors:
            serialized, err, code = sfc.get(s.id, ['measurements', 'latest_readings'])
            if err:
                pass

            data.append(serialized)

    if not len(data):
        data = None

    return render_template('room/sensors.html',
                title='Room Sensors',
                payload=data)


@bp.route('/create', methods=['GET','POST'])
@bp.route('/<pk>/edit', methods=['GET','POST'])
@jwt_required
def edit(pk=None):
    obj = None
    title = 'Add Room'
    schedules = None

    if pk:
        title = 'Edit Room'
        obj = Room.query.get_or_404(pk)

    form = RoomForm(obj=obj)
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            r = Room(name=form.name.data)
            db.session.add(r)

        db.session.commit()

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect(url_for('room.index'))

    return render_template('room/form.html',
        form=form,
        title=title,
        pk=pk)


@bp.route('/<pk>/delete', methods=['POST'])
@jwt_required
def delete(pk):
    r = Room.query.get_or_404(int(pk))
    db.session.delete(r)
    db.session.commit()

    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for('room.index'))
