import json
import hashlib
import logging
from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from sqlalchemy.orm import relationship
from potnanny.core.database import Base, db_session
from potnanny.core.schemas.outlet import GenericOutletSchema
from potnanny.core.utils import subprocess_command
from vesync_outlet import Vesync

logger.getLogger(__name__)

class OutletSetting(Base):
    __tablename__ = 'outlet_settings'

    id = Column(Integer, primary_key=True)
    vesync_enabled = Column(Boolean, nullable=False, default=True)
    rf_enabled = Column(Boolean, nullable=False, default=False)
    rf_tx_pin = Column(Integer, nullable=False, default=0)
    rf_rx_pin = Column(Integer, nullable=False, default=2)
    rf_pulse_width = Column(Integer, nullable=False, default=180)
    created = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<OutletSetting({})>".format(self.id)


class VesyncAccount(Base):
    __tablename__ = 'vesync_accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)
    created = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<VesyncAccount({})>".format(self.username)

    def set_password(self, pw):
        self.password = hashlib.md5(pw.encode('utf-8')).hexdigest()
        db_session.commit()

    def check_password(self, pw):
        return hashlib.md5(pw.encode('utf-8')).hexdigest() == self.password


"""
# WirelessOutlet
Store information about defined wireless (RF) outlets.

## attributes
 - name (required, unique): the name for the outlet.
 - type (required): by default, all wireless outlets have a type of 'wireless'.
 - on_code: a string used by OutletController to send 'ON' codes to the outlet
   via RF signal. Like '1234567890 1 24' (code, protocol, bits)
 - off_code: same as on_code, but for turning the outlet off.
 - state: on=True, off=False
 - created: datetime the device was entered into the database

"""
class WirelessOutlet(Base):
    __tablename__ = 'wireless_outlets'

    id = Column(Integer, primary_key=True)
    name = Column(String(48), nullable=False, unique=True)
    type = Column(String(24), nullable=False, default='wireless')
    on_code = Column(String(24), nullable=False)
    off_code = Column(String(24), nullable=False)
    state = Column(Boolean, nullable=False, default=True)
    created = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<WirelessOutlet({})>".format(self.name)


class FutureOutletAction(Base):
    __tablename__ = 'future_outlet_actions'

    id = Column(Integer, primary_key=True)
    action = Column(String(16), nullable=False, default="off")
    outlet = Column(String(64), nullable=False)
    created = Column(DateTime, default=func.now())
    run_at = Column(DateTime, nullable=False)
    completed = Column(DateTime)

    def __repr__(self):
        return "<FutureOutletAction({})>".format(self.id)


class OutletController(object):
    def __init__(self, *args, **kwargs):
        logger.debug("initializing outlet controller")
        self.vesync = None
        self.settings = None


    def init_vesync(self):
        account = VesyncAccount.query.first()
        if account:
            self.vesync = Vesync(account.username, account.password)
        else:
            raise RuntimeError("No Vesync account exists")


    def available_outlets(self):
        outlets = []
        self.settings = OutletSetting.query.first()
        if not self.settings:
            settings = OutletSetting()
            db_session.add(settings)
            db_session.commit()
            self.settings = settings

        if self.settings.vesync_enabled:
            self.init_vesync()

            devices, response = self.vesync.get_outlets()
            if response == 200:
                outlets += GenericOutletSchema(many=True).load(devices)

        if self.settings.rf_enabled:
            results = WirelessOutlet.query.all()
            if results:
                outlets += GenericOutletSchema(many=True).load(results)

        logger.debug("outlets found: '{}'".format(outlet))
        return outlets


    """
    turn an outlet ON

    params:
        outlet data, like {'id': '1', 'name': 'foo', 'type': 'wireless'}
    returns
        True|False on failure
    """
    def turn_on(self, outlet):
        logger.debug("turning outlet '{}' ON".format(outlet))
        return self.switch_outlet(outlet, 1)


    """
    turn an outlet OFF

    params:
        outlet data, like {'id': '1', 'name': 'foo', 'type': 'wireless'}
    returns
        True|False on failure
    """
    def turn_off(self, outlet):
        logger.debug("turning outlet '{}' OFF".format(outlet))
        return self.switch_outlet(outlet, 0)


    def switch_outlet(self, outlet, state):
        if outlet['type'] in ['vesync', 'wifi-switch']:
            results, response = self.vesync._switch_outlet(outlet['id'], state)
            if response == 200:
                return True

            return False

        if outlet['type'] == 'wireless':
            device = WirelessOutlet.query.get(int(outlet['id']))
            if not device:
                raise RuntimeError("WirelessOutlet '{}' not found".format(outlet['id']))

            code = device.on_code
            if state == 0:
                code = device.off_code

            code, protocol, bits = code.split()
            pw = self.settings.rf_pulse_width
            pin = self.settings.rf_tx_pin

            rval, output, errors = subprocess_command(['/var/www/potnanny/bin/rf_send',
                code, protocol, pw, pin])

            if rval:
                return False

            return True
