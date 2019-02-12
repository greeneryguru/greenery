from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from .models import PollSetting
from potnanny.core.schemas import PollSettingSchema
from potnanny.apps.base import CrudBase

bp = Blueprint('pollsetting_api', __name__, url_prefix='/api/1.0/pollsettings')
api = Api(bp)


ifc = CrudBase(PollSetting, PollSettingSchema)


class PollSettingListApi(Resource):
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    def post(self):
        data, errors = GrowSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class PollSettingApi(Resource):
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk):
        data, errors = GrowSchema().load(request.get_json())
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



api.add_resource(PollSettingListApi, '')
api.add_resource(PollSettingApi, '/<int:pk>')
