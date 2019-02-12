from flask import Blueprint, render_template, redirect, request, url_for
from potnanny.core.models import Action
from potnanny.core.schemas import ActionSchema
from .forms import ActionForm
from potnanny.apps.base import CrudBase
from potnanny.extensions import db

view = Blueprint('action', __name__, template_folder='templates',
                    url_prefix='/actions')
ifc = CrudBase(Action, ActionSchema)


@view.route('/', methods=['GET'])
def index():
    serialized, err, code = ifc.get()
    if err:
        pass

    return render_template('action/index.html',
                title='Action',
                payload=serialized)


@view.route('/create', methods=['GET','POST'])
@view.route('/<pk>/edit', methods=['GET','POST'])
def edit(pk=None):
    obj = None
    title = 'Add Action'
    schedules = None

    if pk:
        title = 'Edit Action'
        obj = Action.query.get_or_404(pk)

    form = ActionForm(obj=obj)
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            r = Action(name=form.name.data)
            db.session.add(r)

        db.session.commit()

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect(url_for('room.index'))

    return render_template('action/form.html',
        form=form,
        title=title,
        pk=pk)
