from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_jwt_extended import jwt_required

from potnanny.core.models import Grow
from potnanny.crud import CrudInterface
from potnanny.core.schemas import GrowSchema
from potnanny.extensions import db
from .forms import GrowForm

bp = Blueprint('grow', __name__,
                    template_folder='templates', url_prefix='/grows')
ifc = CrudInterface(Grow, GrowSchema)

@bp.route('/', methods=['GET'])
@jwt_required
def index():
    serialized, err, code = ifc.get()
    if err:
        pass

    return render_template('grow/index.html',
                title='Rooms',
                payload=serialized)


@bp.route('/<int:pk>', methods=['GET'])
@jwt_required
def get(pk):
    serialized, err, code = ifc.get(pk)
    if err:
        pass

    return jsonify(serialized)


@bp.route('/create', methods=['GET','POST'])
@bp.route('/<pk>/edit', methods=['GET','POST'])
@jwt_required
def edit(pk=None):
    obj = None
    title = 'Add Grow'
    schedules = None

    if pk:
        title = 'Edit Grow'
        obj = Grow.query.get_or_404(pk)

    form = GrowForm(obj=obj)
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            r = Grow(name=form.name.data)
            db.session.add(r)

        db.session.commit()

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect(url_for('room.index'))

    return render_template('grow/form.html',
        form=form,
        title=title,
        pk=pk)


@bp.route('/<pk>/delete', methods=['POST'])
@jwt_required
def delete(pk):
    obj = Grow.query.get_or_404(int(pk))
    db.session.delete(obj)
    db.session.commit()

    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for('grow.index'))
