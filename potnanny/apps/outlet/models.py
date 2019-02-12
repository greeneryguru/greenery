import requests
import hashlib
from potnanny.extensions import db
from sqlalchemy import func
from potnanny.apps.rfi.models import RFIManager
from potnanny.core.schemas import RFOutletSchema
from potnanny.core.models import Error


class OutletSetting(db.Model):
    __tablename__ = 'outlet_settings'

    id = db.Column(db.Integer, primary_key=True)
    rf_enabled = db.Column(db.Boolean, nullable=False, default=False)
    vesync_enabled = db.Column(db.Boolean, nullable=False, default=True)
    vesync_user = db.Column(db.String(48))
    vesync_pass = db.Column(db.String(256))

    def set_password(self, password):
        self.vesync_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        db.session.commit()


class RFOutlet(db.Model):
    __tablename__ = 'rf_outlets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), nullable=False, unique=True)
    type = db.Column(db.String(24), nullable=False, default='wireless')
    on_code = db.Column(db.String(24), nullable=False)
    off_code = db.Column(db.String(24), nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=func.now())


class OutletController(object):
    def __init__(self):
        obj = OutletSetting.query.get(1)
        if not obj:
            obj = OutletSetting()
            db.session.add(obj)
            db.session.commit()

        self.settings = obj
        self.vesync = None

        if self.settings.vesync_enabled:
            try:
                self.vesync = Vesync(self.settings.vesync_user,
                                        self.settings.vesync_pass)
            except Exception as err:
                e = Error(
                    title='vesync interface unexpected error',
                    message='{}'.format(err)
                )
                db.session.add(e)
                db.session.commit()



    """
    List which types of available outlets system is configured to manage.
    """
    def available_types(self):
        data = []
        if self.settings.rf_enabled:
            data.append('wireless')

        if self.settings.vesync_enabled:
            data.append('wifi-switch')


    """
    Get list of all outlets. Only generic detail provided.
    [ {'id': 'id', 'type': 'wireless|vesync|wifi-switch', 'name': name }, ]
    """
    def all_outlets(self):
        outlets = []

        if self.settings.rf_enabled:
            results = RFOutlet.query.all()
            devices, errors = GenericOutletSchema(many=True).dump(results)
            if errors:
                pass
            else:
                outlets += devices

        if self.vesync:
            data, response = self.vesync.get_devices()
            if not data:
                pass
            else:
                devices, errors = GenericOutletSchema(many=True).load(data)
                if not errors:
                    outlets += devices

        return outlets


    """
    extract more detailed information from a generic outlet dict

    params:
        a generic outlet dict
    returns:
        a dict containing more details, including state and on/off codes, etc
    """
    def outlet_details(self, data):
        if data['type'] == 'wireless':
            obj = RFOutlet.query.get(int(data['id']))
            if not obj:
                return None
            data, error = RFOutletSchema().load(obj)
            if not error:
                return data

        elif data['type'] in ['vesync', 'wifi-switch']:
            bulk, response = self.vesync.get_outlets()
            if bulk:
                for d in bulk:
                    if d['id'] == data['id']:
                        ser, err = VesyncOutletSchema().load(d)
                        if not err:
                            return ser

        return None


    """
    switch an outlet ON

    params:
        a generic outlet dict, like:
            {'id': 'ID', 'name': 'OUTLET NAME', 'type': 'OUTLET TYPE'}
    returns:
        0 on success, non-zero on failure
    """
    def switch_on(self, data):
        if data['type'] == 'wireless':
            return self._wireless_switch(self, data, 1)

        elif data['type'] in ['vesync', 'wifi-switch']:
            data, response = self.vesync.turn_on(id)
            if not errors:
                return 0
            else:
                e = Error(
                    title='wifi switch error',
                    message='failed to switch a wifi outlet. {}, {}'.format(
                        response.status_code,
                        response.headers)
                )
                db.session.add(e)
                db.session.commit()
                return 1

    """
    switch an outlet OFF

    params:
        a generic outlet dict, like:
            {'id': 'ID', 'name': 'OUTLET NAME', 'type': 'OUTLET TYPE'}
    returns:
        0 on success, non-zero on failure
    """
    def switch_off(self, data):
        if data['outlet_type'] == 'wireless':
            return self._wireless_switch(self, id, 0)

        elif data['type'] in ['vesync', 'wifi-switch']:
            data, errors = self.vesync.turn_off(id)
            if not errors:
                return 0
            else:
                e = Error(
                    title='wifi switch error',
                    message='failed to switch a wifi outlet. {}, {}'.format(
                        response.status_code,
                        response.headers)
                )
                db.session.add(e)
                db.session.commit()
                return 1


    def _wireless_switch(self, data, state):
        obj = RFOutlet.query.get( int( data['id'] ) )
        mgr = RFIManager()

        try:
            if state:
                rval, msg = mgr.send_code(obj.on_code)
            else:
                rval, msg = mgr.send_code(obj.off_code)

            if not rval:
                obj.state = state
                db.session.commit()
            else:
                e = Error(
                    title='wireless switch error',
                    message='failed to switch a wireless outlet. ' + msg
                )
                db.session.add(e)
                db.session.commit()

            return rval

        except Exception as err:
            e = Error(
                title='wireless switch unexpected failure',
                message='failed to switch a wireless outlet. ' + err
            )
            db.session.add(e)
            db.session.commit()

            return -1
