from flask import Blueprint, render_template, redirect, request, url_for
from flask_jwt_extended import jwt_required

from potnanny.core.models import Room
from potnanny.core.schemas import RoomSchema
from potnanny.crud import CrudInterface
from potnanny.extensions import db

bp = Blueprint('dashboard', __name__, template_folder='templates')
ifc = CrudInterface(Room, RoomSchema)

@bp.route('/', methods=['GET'])
@jwt_required
def index():
    serialized, err, code = ifc.get()
    if err:
        pass

    return render_template('dashboard/index.html',
                title='Dashboard',
                rooms=serialized)


@bp.route('/<int:pk>', methods=['GET'])
@jwt_required
def edit(pk):
    serialized, err, code = ifc.get(pk)
    if err:
        pass

    return render_template('dashboard/edit.html',
                title='Customize Room',
                room=serialized)
