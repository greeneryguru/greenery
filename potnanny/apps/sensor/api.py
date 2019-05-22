from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from potnanny_core.models import Sensor
from .schemas import SensorSchema
from potnanny.crud import CrudInterface


bp = Blueprint('sensor_api', __name__, url_prefix='/api/1.0/sensors')
# api = Api(bp, decorators=[csrf_protect.exempt])
api = Api(bp)

class SensorListApi(Resource):
    # @jwt_required
    def get(self):
        sensors = Sensor.query.all()
        if not sensors:
            return {"message": "no data"}, 404

        serialized, errors = SensorSchema(many=True).dump(sensors)
        if errors:
            return errors, 400

        return serialized, 200


class SensorApi(Resource):
    # @jwt_required
    def get(self, pk):
        sensor = Sensor.query.get(pk)
        if not sensor:
            return {"message": "object does not exist"}, 404

        serialized, errors = SensorSchema().dump(room)
        if errors:
            return errors, 400

        return serialized, 200

    # @jwt_required
    def put(self, pk):
        data, errors = SensorSchema().load(request.get_json())
        if errors:
            return errors, 400

        sensor = Sensor.query.get(pk)
        if not sensor:
            return {"message": "object does not exist"}, 404

        db_session.commit()
        serialized, errors = SensorSchema().dump(sensor)
        if errors:
            return errors, 400

        return serialized, 200

    # @jwt_required
    def delete(self, pk):
        sensor = Sensor.query.get(pk)
        if not sensor:
            return {"message": "object does not exist"}, 404

        db_session.delete(sensor)
        db_session.commit()
        return "", 204


api.add_resource(SensorListApi, '')
api.add_resource(SensorApi, '/<int:pk>')
