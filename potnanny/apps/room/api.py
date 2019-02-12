from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny.core.models import Room
from potnanny.core.schemas import RoomSchema
from potnanny.crud import CrudInterface


bp = Blueprint('room_api', __name__, url_prefix='/api/1.0/rooms')
api = Api(bp)
ifc = CrudInterface(Room, RoomSchema)

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
        ser, err, code = ifc.get(pk, ['environment','environment'])
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


api.add_resource(RoomListApi, '')
api.add_resource(RoomApi, '/<int:pk>')
