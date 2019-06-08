from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models.schedule import (ScheduleOnOff, RoomLightManager)
from potnanny_core.schemas.schedule import ScheduleOnOffSchema
from potnanny_core.database import db_session
from potnanny_api.crud import CrudInterface

bp = Blueprint('schedule_api', __name__, url_prefix='/api/1.0/schedules')
api = Api(bp)
ifc = CrudInterface(db_session, ScheduleOnOff, ScheduleOnOffSchema)

class ScheduleListApi(Resource):
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    def post(self):
        data, errors = ScheduleOnOffSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class ScheduleApi(Resource):
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    def put(self, pk):
        data, errors = ScheduleOnOffSchema().load(request.get_json())
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


api.add_resource(ScheduleListApi, '')
api.add_resource(ScheduleApi, '/<int:pk>')
