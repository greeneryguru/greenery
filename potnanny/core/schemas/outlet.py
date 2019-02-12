from marshmallow import Schema, fields, validates


class GenericOutletSchema(Schema):
    class META:
        strict = True

    id = fields.Str()
    name = fields.Str(load_from='deviceName')
    type = fields.Str()

    @validates('type')
    def validate_type(self, value):
        allowed = ['wireless', 'wifi-switch', 'vesync']
        if value not in allowed:
            raise ValidationError(
                "outlet type must be one of [{}]".format(",".join(allowed)))


class WirelessOutletSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(dump_only=True)
    on_code = fields.Str(required=True)
    off_code = fields.Str(required=True)
    state = fields.Boolean(dump_only=True)
    created = fields.DateTime(dump_only=True)


class VesyncOutletSchema(Schema):
    class META:
        strict = True

    id = fields.String(dump_only=True)
    name = fields.Str(required=True, load_from='deviceName')
    type = fields.Str(dump_only=True)
    relay = fields.Str()
    status = fields.Str(dump_only=True)
    state = fields.Method("calc_state")

    def calc_state(self, obj):
        if 'relay' in obj and obj.relay == 'open':
            return True

        return False


class OutletSettingSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    vesync_enabled = fields.Boolean()
    rf_enabled = fields.Boolean()
    rf_pulse_width = fields.Integer()
    rf_tx_pin = fields.Integer()
    rf_rx_pin = fields.Integer()
