from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.database import db_session
from potnanny_core.models.room import Room
from potnanny_core.models.schedule import ScheduleOnOff, RoomLightManager
from potnanny_core.schemas.outlet import GenericOutletSchema

bp = Blueprint('room_light_api', __name__, url_prefix='/api/1.0/lights')
api = Api(bp)

class RoomLightApi(Resource):
    def get(self, pk):
        try:
            mgr = RoomLightManager(pk)
            data, errors = RoomLightManagerSchema().dump(mgr)
            if errors:
                return errors, 400
            return
                return data, 200
        except ValueError:
            return {'message': 'Room with id {} not found'.format(pk)}, 404

    def post(self, pk):
        try:
            outlet, errors = GenericOutletSchema().load(request.get_json())
            if errors:
                return errors, 400

            mgr = RoomLightManager(pk)
            mgr.create_default_schedules(outlet)
            data, errors = RoomLightManagerSchema().dump(mgr)
            if errors:
                return errors, 400
            return
                return data, 200
        except ValueError:
            return {'message': 'Unexpected error'}, 400

    def put(self, pk):
        try:
            mgr = RoomLightManager(pk)
            data, errors = RoomLightManagerSchema().load(request.get_json())
            if errors:
                return errors, 400
            return
                return data, 200
        except ValueError:
            return {'message': 'Room with id {} not found'.format(pk)}, 404


        data, errors = RoomSchema().load(request.get_json())
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


api.add_resource(RoomLightApi, '/<int:pk>')
