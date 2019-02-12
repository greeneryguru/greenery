from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from .models import RFISetting
from potnanny.core.schemas import RFISettingSchema
from potnanny.apps.base import CrudBase

bp = Blueprint('rfi_api', __name__, url_prefix='/api/1.0/rfi')
# api = Api(bp, decorators=[csrf_protect.exempt])
api = Api(bp)
ifc = CrudBase(RFISetting, RFISettingSchema)


class RFISettingListApi(Resource):
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code


class RFISettingApi(Resource):
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk):
        data, errors = RFISettingSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(pk, data)
        if err:
            return err, code

        return ser, code


class RFIScanApi(Resource):
    def get(self):
        mgr = RFIManager()
        rval, msg = mgr.scan_code()
        if not rval:
            return {"code": msg}, 200

        return {"message": "RFIManager scan failure. {}".format(msg)}, 400

api.add_resource(RFISettingListApi, '')
api.add_resource(RFISettingApi, '/<int:pk>')
api.add_resource(RFIScanApi, '/scan')
