import json
import copy
import marshmallow
from marshmallow import Schema, fields, validates, ValidationError


class ActionSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    created = fields.DateTime(dump_only=True)
    is_active = fields.Boolean()
    room_id = fields.Integer()
    measurement_type = fields.Str(required=True)
    sensor = fields.Str(required=True)
    data = fields.Str(required=True)
    triggers = fields.Nested('TriggerSchema', exclude=['action'], dump_only=True, many=True)
