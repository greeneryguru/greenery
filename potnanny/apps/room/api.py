from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models import Room
from .schemas import RoomSchema

bp = Blueprint('room_api', __name__, url_prefix='/api/1.0/rooms')
api = Api(bp)


class RoomListApi(Resource):
    # @jwt_required
    def get(self):
        rooms = Room.query.all()
        if not rooms:
            return {"message": "no data"}, 404

        serialized, errors = RoomSchema(many=True).dump(rooms)
        if errors:
            return errors, 400

        return serialized, 200

    # @jwt_required
    def post(self):
        data, errors = RoomSchema().load(request.get_json())
        if errors:
            return errors, 400

        room = Room(**data)
        db_session.add(room)
        db_session.commit()
        serialized, errors = RoomSchema().dump(room)
        if errors:
            return errors, 400

        return serialized, 200


class RoomApi(Resource):
    # @jwt_required
    def get(self, pk, incl_env=True):
        room = Room.query.get(pk)
        if not room:
            return {"message": "object does not exist"}, 404

        serialized, errors = RoomSchema().dump(room)
        if errors:
            return errors, 400

        if incl_env:
            serialized['environment'] = room.environment()

        return serialized, 200

    # @jwt_required
    def put(self, pk):
        data, errors = RoomSchema().load(request.get_json())
        if errors:
            return errors, 400

        room = Room.query.get(pk)
        if not room:
            return {"message": "object does not exist"}, 404

        db_session.commit()
        serialized, errors = RoomSchema().dump(room)
        if errors:
            return errors, 400

        return serialized, 200

    # @jwt_required
    def delete(self, pk):
        room = Room.query.get(pk)
        if not room:
            return {"message": "object does not exist"}, 404

        db_session.delete(room)
        db_session.commit()
        return "", 204


api.add_resource(RoomListApi, '')
api.add_resource(RoomApi, '/<int:pk>')
