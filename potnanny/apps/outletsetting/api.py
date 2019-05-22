from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from potnanny_core.models import OutletSetting
from .schemas import OutletSettingSchema
from potnanny.crud import CrudInterface


bp = Blueprint('outletsetting_api', __name__, url_prefix='/api/1.0/outletsettings')
api = Api(bp)
ifc = CrudInterface(OutletSetting, OutletSettingSchema)


class OutletSettingApi(Resource):
    def get(self, pk=1):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk=1):
        data, errors = OutletSettingSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(pk, data)
        if err:
            return err, code

        return ser, code


api.add_resource(OutletSettingApi, '')
