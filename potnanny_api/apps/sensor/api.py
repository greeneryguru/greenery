from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models.sensor import Sensor
from potnanny_core.schemas.sensor import SensorSchema
from potnanny_core.database import db_session
from potnanny_api.crud import CrudInterface

bp = Blueprint('sensor_api', __name__, url_prefix='/api/1.0/sensors')
api = Api(bp)
ifc = CrudInterface(db_session, Sensor, SensorSchema)

class SensorListApi(Resource):
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    def post(self):
        data, errors = SensorSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class SensorApi(Resource):
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk):
        data, errors = SensorSchema().load(request.get_json())
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



api.add_resource(SensorListApi, '')
api.add_resource(SensorApi, '/<int:pk>')
