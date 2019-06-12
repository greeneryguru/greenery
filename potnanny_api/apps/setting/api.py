import json
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models.setting import (PollingInterval, TemperatureDisplay,
    VesyncAccount, PrimitiveWirelessSetting)
from potnanny_core.schemas.keychain import KeychainSchema
from potnanny_core.schemas.setting import (PollingIntervalSchema,
    TemperatureDisplaySchema, PrimitiveWirelessSettingSchema,
    VesyncAccountSchema)


bp = Blueprint('settings_api', __name__, url_prefix='/api/1.0/settings')
api = Api(bp)


class SettingListApi(Resource):

    @jwt_required
    def get(self):
        data = []
        possibles = ['polling_interval', 'temperature_display',
            'primitive_wireless', 'vesync_account']

        keys = Keychain.query.all()
        if len(keys) < 1:
            return {"message": "no data"}, 404

        for obj in keys:
            if obj.name in possibles:
                data.append(obj)

        serialized, errors = KeychainSchema(many=True).dump(data)
        if errors:
            return errors, 400
        else:
            return serialized, 200


class SettingApi(Resource):

    @jwt_required
    def get(self, name):
        obj = None
        serialized = None
        errors = None

        if name == 'polling_interval':
            obj = PollingInterval.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = PollingIntervalSchema().load(json.loads(obj.data))

        elif name == 'temperature_display':
            obj = TemperatureDisplay.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = TemperatureDisplaySchema().load(json.loads(obj.data))

        elif name == 'primitive_wireless':
            obj = PrimitiveWirelessSetting.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = PrimitiveWirelessSettingSchema().load(json.loads(obj.data))

        elif name == 'vesync_account':
            obj = VesyncAccount.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = VesyncAccountSchema().load(json.loads(obj.data))

        else:
            return {"message": "Unexpected setting type"}, 404


        if errors:
            return errors, 400

        return serialized, 200


    @jwt_required
    def put(self, name):
        data = None
        errors = None

        if name == 'polling_interval':
            data, errors = PollingIntervalSchema().load(request.get_json())
            if errors:
                return errors, 400

            PollingInterval.set()
            obj = PollingInterval.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = PollingIntervalSchema().dump(json.loads(obj.data))

        elif name == 'temperature_display':
            obj = TemperatureDisplay.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = TemperatureDisplaySchema().dump(json.loads(obj.data))

        elif name == 'primitive_wireless':
            obj = PrimitiveWirelessSetting.get()
            if not obj:
                return {"message": "object not found"}, 404

            serialized, errors = PrimitiveWirelessSettingSchema().dump(json.loads(obj.data))
        else:
            return {"message": "Unexpected setting type"}, 404


        data, errors = SensorSchema().load(request.get_json())
        if errors:
            return errors, 400

        sensor = Sensor.query.get(pk)
        if not sensor:
            return {"message": "object does not exist"}, 404

        db_session.commit()
        serialized, errors = SensorSchema().dump(sensor)
        if errors:
            return errors, 400

        return serialized, 200

    @jwt_required
    def delete(self, name):
        obj = Keychain.query.filter_by(name=name).first()
        if obj:
            db_session.delete(obj)
            db_session.commit()

        return "", 204


api.add_resource(SettingListApi, '/settings')
api.add_resource(SettingApi, '/settings/<key>')
