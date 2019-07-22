import datetime
from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models.grow import Grow
from potnanny_core.models.schedule import RoomLightManager
from potnanny_core.schemas.grow import GrowSchema
from potnanny_core.database import db_session
from potnanny_api.crud import CrudInterface


bp = Blueprint('grow_api', __name__, url_prefix='/api/1.0/grows')
api = Api(bp)
ifc = CrudInterface(db_session, Grow, GrowSchema)

class GrowListApi(Resource):

    #@jwt_required
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    #@jwt_required
    def post(self):
        data, errors = GrowSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        try:
            mgr = RoomLightManager(ser['id'])
            mgr.switch_to_phase('growth')
        except:
            pass
        return ser, code


class GrowApi(Resource):

    #@jwt_required
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    #@jwt_required
    def put(self, pk):
        data, errors = GrowSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(pk, data)
        if err:
            return err, code

        return ser, code

    #@jwt_required
    def delete(self, pk):
        ser, err, code = ifc.delete(pk)
        if err:
            return err, code

        return ser, code


class GrowApiSwitch(Resource):

    #@jwt_required
    def post(self, pk):
        data = request.get_json()
        if not data or 'phase' not in data:
            return {'msg': 'Invalid POST data'}, 400

        if data['phase'] not in ['growth', 'flowering', 'end']:
            return {'msg': 'Growth phase POST data option invalid'}, 400

        grow = Grow.query.get(pk)
        if not grow:
            return {'msg': 'Grow id not found'}, 404

        mgr = RoomLightManager(grow.room_id)
        if data['phase'] == 'growth':
            # this is an odd scenario. transitioning from flower back to grow?
            # user must have made mistake. anyway, reset datetime fields.
            if grow.transitioned is not None:
                grow.transitioned = None
            grow.started = datetime.datetime.utcnow()

            try:
                if mgr.schedules() is not None:
                    mgr.switch_to_phase('growth')
            except:
                # TODO: log an error here?
                pass
        elif data['phase'] == 'flowering':
            grow.transitioned = datetime.datetime.utcnow()
            try:
                if mgr.schedules() is not None:
                    mgr.switch_to_phase('flowering')
            except:
                # TODO: log an error here?
                pass
        elif data['phase'] == 'end':
            grow.ended = datetime.datetime.utcnow()
            # TODO: run a data aggregation job in backround? To create some
            # type of report?

        db_session.commit()
        data, errors = GrowSchema().load(grow)
        if not errors:
            return data, 201
        else:
            errors, 400


api.add_resource(GrowListApi, '')
api.add_resource(GrowApi, '/<int:pk>')
api.add_resource(GrowApiSwitch, '/<int:pk>/switch')
