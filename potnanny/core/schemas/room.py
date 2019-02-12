from marshmallow import Schema, fields


class RoomSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(
                dump_only=True)
    name = fields.Str(
                required=True,
                error_messages={'required': 'Name is required'})
    created = fields.DateTime(
                dump_only=True)
    notes = fields.Str()
    environment = fields.Dict(dump_only=True)
    sensors = fields.Nested('SensorSchema', many=True, dump_only=True, exclude=['room'])
    actions = fields.Nested('ActionSchema', many=True, dump_only=True, exclude=['room'])
    grows = fields.Nested('GrowSchema', many=True, dump_only=True, exclude=['room'])
    # outlets = fields.Nested('RFOutletSchema', many=True, dump_only=True, exclude=['room'])
