from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models.action import Action
from potnanny_core.schemas.action import ActionSchema
from potnanny_core.database import db_session
from potnanny_api.crud import CrudInterface


bp = Blueprint('action_api', __name__, url_prefix='/api/1.0/actions')
api = Api(bp)
ifc = CrudInterface(db_session, Action, ActionSchema)


class ActionListApi(Resource):
    """Class to interface with Actions."""

    @jwt_required
    def get(self):
        """Get list of all actions."""

        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    @jwt_required
    def post(self):
        """Post/Edit Action."""

        data, errors = ActionSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class ActionApi(Resource):

    @jwt_required
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    @jwt_required
    def put(self, pk):
        data, errors = ActionSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(pk, data)
        if err:
            return err, code

        return ser, code

    @jwt_required
    def delete(self, pk):
        ser, err, code = ifc.delete(pk)
        if err:
            return err, code

        return ser, code


api.add_resource(ActionListApi, '')
api.add_resource(ActionApi, '/<int:pk>')
