from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from potnanny.core.models import Action
from potnanny.core.schemas import ActionSchema
from potnanny.apps.base import CrudBase


bp = Blueprint('action_api', __name__, url_prefix='/api/1.0/actions')
# api = Api(bp, decorators=[csrf_protect.exempt])
api = Api(bp)
ifc = CrudBase(Action, ActionSchema)


class ActionListApi(Resource):
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    def post(self):
        data, errors = ActionSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class ActionApi(Resource):
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk):
        data, errors = ActionSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(pk, data)
        if err:
            return err, code

        return ser, code

    def delete(self, pk):
        ser, err, code = ifc.delete(pk)
        if err:
            return err, code

        return ser, code


api.add_resource(ActionListApi, '')
api.add_resource(ActionApi, '/<int:pk>')
