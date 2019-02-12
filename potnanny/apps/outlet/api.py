from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from .models import RFOutlet, OutletController
from potnanny.core.schemas import RFOutletSchema
from potnanny.apps.base import CrudBase


bp = Blueprint('outlet_api', __name__, url_prefix='/api/1.0/outlets')
# api = Api(bp, decorators=[csrf_protect.exempt])
api = Api(bp)
ifc = CrudBase(RFOutlet, RFOutletSchema)


class OutletListApi(Resource):
    def get(self):
        http_code = 200
        oc = OutletController()
        results = oc.list_all()

        return results, http_code

    def post(self):
        data, errors = RFOutletSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class OutletApi(Resource):
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk):
        data, errors = RFOutletSchema().load(request.get_json())
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


api.add_resource(OutletListApi, '')
api.add_resource(OutletApi, '/<id>')
