from marshmallow import Schema, fields
import potnanny.core.schemas


class SensorSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(
                dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(dump_only=True)
    model = fields.Str(dump_only=True)
    room_id = fields.Integer()
    created = fields.DateTime(dump_only=True)
    measurement_codes = fields.Dict(dump_only=True)
