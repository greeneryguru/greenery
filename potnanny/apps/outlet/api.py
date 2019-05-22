from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from potnanny_core.models import OutletController, WirelessOutlet
from potnanny_core.schemas import GenericOutletSchema, WirelessOutletSchema
from potnanny.crud import CrudInterface


bp = Blueprint('outlet_api', __name__, url_prefix='/api/1.0/outlets')
api = Api(bp)
ifc = CrudInterface(WirelessOutlet, WirelessOutletSchema)
oc = OutletController()


class OutletListApi(Resource):
    # get all outlets available on this system
    def get(self):
        http_code = 200
        results = oc.available_outlets()

        return results, http_code

    # create new wireless outlet
    def post(self):
        data, errors = WirelessOutletSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class OutletApi(Resource):
    def get(self, id):
        outlet = oc.get_outlet(id)
        if outlet is None:
            return {'message': 'outlet not found'}, 404

        return outlet, 200


    def put(self, pk):
        # only WirelessOutlets can be modified
        if type(pk) is not int and not pk.isdigit():
            return {'message': 'invalid outlet id for this operation'}, 400

        data, errors = WirelessOutletSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(int(pk), data)
        if err:
            return err, code

        return ser, code

    def delete(self, pk):
        if type(pk) is not int and not pk.isdigit():
            return {'message': 'invalid outlet id for this operation'}, 400

        ser, err, code = ifc.delete(int(pk))
        if err:
            return err, code

        return ser, code

class OutletSwitchApi(Resource):
    def post(self):
        data, errors = GenericOutletSchema().load(request.get_json())
        if errors:
            return errors, 400

        oc = OutletController()
        result = oc.switch_outlet(data)

        if result:
            return data, 200
        else:
            return {'message': 'failed to switch outlet'}, 400


api.add_resource(OutletListApi, '')
api.add_resource(OutletApi, '/<id>')
api.add_resource(OutletSwitchApi, '/switch')
