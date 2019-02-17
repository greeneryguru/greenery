from flask import Blueprint, request, url_for
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from potnanny_core.models import User
from .schema import UserSchema

bp = Blueprint('user_api', __name__, url_prefix='/api/1.0/users')
api = Api(bp)

class UserListApi(Resource):
    # GET list of all users
    @jwt_required
    def get(self):
        results = User.query.all()
        if not results:
            return {"msg": "no users"}, 404

        data, errors = UserSchema(many=True).dump(results)
        if errors:
            return errors, 404

        return data, 200

    # POST create a new user
    @jwt_required
    def post(self):
        password = request.get_json()['password']
        if not password or password == "":
            return {"msg": "password required"}, 400

        data, errors = UserSchema().load(request.get_json())
        if errors:
            return errors, 400

        obj = User(**data)
        obj.set_password(data['password'])
        db.session.add(obj)
        db.session.commit()

        serialized, errors = UserSchema().dump(obj)
        if errors:
            return errors, 400

        return serialized, 200


class UserApi(Resource):
    # GET an existing user
    @jwt_required
    def get(self, pk):
        obj = User.query.get(pk)
        data, errors = UserSchema().dump(obj)
        if errors:
            return errors, 400

        return data, 200

    # EDIT an existing user
    @jwt_required
    def put(self, pk):
        obj = User.query.get(pk)
        data, errors = UserSchema().load(request.get_json())
        if errors:
            return errors, 400

        for k, v in data.items():
            setattr(obj, k, v)

        db.session.commit()
        data, errors = UserSchema().dump(obj)
        if errors:
            return errors, 400

        return data, 200

    # DELETE an existing user
    @jwt_required
    def delete(self, pk):
        obj = User.query.get(pk)
        if not obj:
            return {"msg": "user does not exist"}, 400
        db.session.delete(obj)
        db.session.commit()

        return "", 204


api.add_resource(UserListApi, '')
api.add_resource(UserApi, '/<int:pk>')
