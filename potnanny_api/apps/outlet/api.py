from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from potnanny_core.models.outlet import OutletController, Outlet
from potnanny_core.models.wireless import WirelessInterface
from potnanny_core.schemas.outlet import GenericOutletSchema, OutletSchema

bp = Blueprint('outlet_api', __name__, url_prefix='/api/1.0/outlets')
api = Api(bp)
oc = OutletController()

class OutletListApi(Resource):
    """Class to interface with Generic Power Outlets."""

    def get(self):
        """Get list of all available outlets."""

        results = oc.available_outlets()
        if not results:
            return {'message': 'no outlets found'}, 404

        data, errors = GenericOutletSchema(many=True).load(results)
        if errors:
            return errors, 400

        return data, 200

    def post(self):
        """Create a new wireless outlet."""

        data, errors = OutletSchema().load(request.get_json())
        if errors:
            return errors, 400

        obj = Outlet(**data)
        db_session.add(obj)
        db_session.commit()

        return OutletSchema().dump(obj), 200


class OutletApi(Resource):
    """Class to Interface with single Generic Power Outlet."""

    def get(self, id):
        """
        Get details of Outlet with id.

        args:
            - str: id of outlet, like ("3" or "123455-56666-18264")
        returns:
            json, http result code
        """

        outlet = oc.get_outlet(id)
        if outlet is None:
            return {'message': 'outlet not found'}, 404

        return outlet, 200


    def put(self, pk):
        """
        Edit details of a Wireless Outlet with id.

        args:
            - int: wireless outlet id number
        returns:
            json, http result code
        """

        if type(pk) is not int and not pk.isdigit():
            return {'message': 'invalid outlet id for this operation'}, 400

        data, errors = OutletSchema().load(request.get_json())
        if errors:
            return errors, 400

        obj = Outlet.query.get(int(pk))
        if not obj:
            return {'message': 'object with id %s not found' % pk}, 404

        for k, v in data.items():
            setattr(obj, k, v)

        db_session.commit()
        data, errors = OutletSchema().load(obj)
        if errors:
            return errors, 400

        return data, 200


    def delete(self, pk):
        """
        Delete a Wireless Outlet with id.

        args:
            - int: wireless outlet id number
        returns:
            json, http result code
        """

        if type(pk) is not int and not pk.isdigit():
            return {'message': 'invalid outlet id for this operation'}, 400

        ser, err, code = ifc.delete(int(pk))
        if err:
            return err, code

        return ser, code


class OutletSwitchApi(Resource):
    """Class to switch outlets ON or OFF."""

    def post(self):
        """Accept post data to switch outlet state to 1 (on) or 0 (off)."""

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
