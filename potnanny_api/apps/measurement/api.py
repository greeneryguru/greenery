from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource

bp = Blueprint('measurement_api', __name__, url_prefix='/api/1.0/measurements')
api = Api(bp)


class MeasurementListApi(Resource):
    def get(self):
        serialized, error, code = get_all()
        if error:
            return error, code

        return serialized, code

    def post(self):
        data, errors = GrowSchema().load(request.get_json())
        if errors:
            return errors, 400

        serialized, error, code = create_obj(data)
        if error:
            return error, code

        return serialized, code


class MeasurementApi(Resource):
    def get(self, pk):
        serialized, error, code = get_obj(pk)
        if error:
            return error, code

        return serialized, code

    def put(self, pk):
        data, errors = GrowSchema().load(request.get_json())
        if errors:
            return errors, 400

        serialized, error, code = edit_obj(pk, data)
        if error:
            return error, code

        return serialized, code

    def delete(self, pk):
        serialized, error, code = obj_del(pk)
        if error:
            return error, code

        return serialized, code


api.add_resource(MeasurementListApi, '')
api.add_resource(MeasurementApi, '/<int:pk>')
