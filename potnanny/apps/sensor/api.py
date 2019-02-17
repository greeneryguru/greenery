from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from potnanny_core.models import Sensor
from .schema import SensorSchema
from potnanny.crud import CrudInterface


bp = Blueprint('sensor_api', __name__, url_prefix='/api/1.0/sensors')
# api = Api(bp, decorators=[csrf_protect.exempt])
api = Api(bp)
ifc = CrudInterface(Sensor, SensorSchema)


class SensorListApi(Resource):
    @jwt_required
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    @jwt_required
    def post(self):
        data, errors = SensorSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class SensorApi(Resource):
    @jwt_required
    def get(self, pk):
        ser, err, code = ifc.get(pk, ['measurement_codes','measurement_codes'])
        if err:
            return err, code

        return ser, code

    @jwt_required
    def put(self, pk):
        data, errors = SensorSchema().load(request.get_json())
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


api.add_resource(SensorListApi, '')
api.add_resource(SensorApi, '/<int:pk>')
