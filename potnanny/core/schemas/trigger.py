from marshmallow import Schema, fields
import potnanny.core.schemas


class TriggerSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True)
    closed = fields.DateTime(dump_only=True)
