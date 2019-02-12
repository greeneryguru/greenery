from marshmallow import Schema, fields


class ErrorSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(
                dump_only=True)
    title = fields.Str(required=True,
                error_messages={'required': 'Title is required'})
    message = fields.Str(required=True,
                error_messages={'required': 'Message is required'})
    created = fields.DateTime(dump_only=True)
