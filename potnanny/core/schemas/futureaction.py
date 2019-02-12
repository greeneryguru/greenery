from marshmallow import Schema, fields, validates
from potnanny.core.schemas import GenericOutletSchema

class FutureOutletActionSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    action = fields.Str(required=True)
    outlet = fields.Nested('GenericOutletSchema')
    created = fields.DateTime(dump_only=True)
    run_at = fields.DateTime(required=True)
    completed = fields.DateTime()

    @validates('action')
    def validate_action(self, value):
        allowed = ['on', 'off']
        if value not in allowed:
            raise ValidationError(
                "action must be in [{}]".format(",".join(allowed))
            )
