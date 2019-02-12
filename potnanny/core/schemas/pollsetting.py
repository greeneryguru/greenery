from marshmallow import Schema, fields

class PollSettingSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    interval = fields.Integer(required=True)
    created = fields.DateTime(dump_only=True)
