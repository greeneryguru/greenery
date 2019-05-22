from marshmallow import Schema, fields


class OutletSettingSchema(Schema):
    class META:
        strict = True

    id = fields.Integer(dump_only=True)
    rf_enabled = fields.Boolean()
    rf_tx_pin = fields.Integer()
    rf_rx_pin = fields.Integer()
    rf_pulse_width = fields.Integer()
    created = fields.DateTime(dump_only=True)
