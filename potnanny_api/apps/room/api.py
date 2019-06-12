from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.database import db_session
from potnanny_core.models.room import Room
from potnanny_core.schemas.room import RoomSchema
from potnanny_core.models.schedule import ScheduleOnOff, RoomLightManager
from potnanny_core.schemas.outlet import GenericOutletSchema
from potnanny_api.crud import CrudInterface

bp = Blueprint('room_api', __name__, url_prefix='/api/1.0/rooms')
api = Api(bp)
ifc = CrudInterface(db_session, Room, RoomSchema)

class RoomListApi(Resource):

    @jwt_required
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    @jwt_required
    def post(self):
        data, errors = RoomSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class RoomApi(Resource):

    @jwt_required
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    @jwt_required
    def put(self, pk):
        data, errors = RoomSchema().load(request.get_json())
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


class RoomLightApi(Resource):
    @jwt_required
    def get(self, pk):
        try:
            mgr = RoomLightManager(pk)
            data, errors = RoomLightManagerSchema().load(mgr)
            if errors:
                return errors, 400
            else:
                return data, 200
        except ValueError:
            return {'message': 'Room with id {} not found'.format(pk)}, 404

    @jwt_required
    def post(self, pk):
        try:
            outlet, errors = GenericOutletSchema().load(request.get_json())
            if errors:
                return errors, 400

            mgr = RoomLightManager(pk)
            mgr.create_default_schedules(outlet)
            data, errors = RoomLightManagerSchema().load(mgr)
            if errors:
                return errors, 400
            else:
                return data, 200
        except ValueError:
            return {'message': 'Unexpected error'}, 400

    @jwt_required
    def put(self, pk):
        try:
            mgr = RoomLightManager(pk)
            data, errors = RoomLightManagerSchema().load(request.get_json())
            if errors:
                return errors, 400
            else:
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

    @jwt_required
    def delete(self, pk):
        ser, err, code = ifc.delete(pk)
        if err:
            return err, code

        return ser, code


api.add_resource(RoomListApi, '')
api.add_resource(RoomApi, '/<int:pk>')
api.add_resource(RoomLightApi, '/<int:pk>/lights')
