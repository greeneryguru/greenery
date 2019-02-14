#!/usr/bin/env python3

import os
import sys
import re
import copy
import time
import json
import logging
import datetime
import argparse

from potnanny.config import Production, Testing, Development
from potnanny.core.database import db_session, init_db, init_engine
from potnanny.core.models import (Measurement, Sensor, Room, Action, Trigger,
    BlePluginBase, ActionPluginBase, PollSetting, OutletController,
    FutureOutletAction)
from potnanny.core.utils import (eval_condition, load_plugins,
    blescan_devices, rehydrate_plugin_instance)


"""
Part of the POTNANNY application.

This poll script should be run every minute in the super-user cron, and does
several things:

 - check for any FutureActions that need to be handled right now. FutureActions
   are, at present, only turning outlets off.

 Depending on the polling interval setting, the script may also do:

 - poll ble devices for new measurements.
 - insert newly found sensors into the database.
 - insert ble device measurements into the database
 - trigger actions based on the measurements

Jeff Leary
potnanny@gmail.com

01/2019
"""


def main():

    # load plugins from paths for ble scan plugins
    logger.debug("loading plugins")
    load_plugins(os.path.join(app_config.POTNANNY_PLUGIN_PATH, 'ble'))
    load_plugins(os.path.join(app_config.POTNANNY_PLUGIN_PATH, 'action'))

    measurements = []
    devices = blescan_devices()
    if devices:
        for cls in BlePluginBase.plugins:
            results = cls.poll(devices)
            if results:
                measurements += results

        if measurements:
            load_measurements(measurements)


"""
add ble sensor device to the database if it is not already present.

params:
    a dict like {'address': 'xx:xx:xx:xx:xx:xx', 'name': 'flower care', }

returns:
    a Sensor object, None on error
"""
def get_or_create_sensor(data):
    obj = Sensor.query.filter_by(address=data['address']).first()
    if not obj:
        logger.debug("create new sensor from '{}'".format(data))
        try:
            obj = Sensor(address=data['address'], model=data['name'])
            db_session.add(obj)
            db_session.commit()
        except Exception:
            logger.exception("create new Sensor failed")

    return obj


"""
load measurement data into database, take actions on the measurements if needed.

params:
    a list of dicts, like:
    [
        {   'address': '11:11:11:11:11',
            'name': 'flower care',
            'measurements': {
                'temperature': 24.2,
                'soil-moisture': 21.0,
                'light': 11300.0,
                'soil-ec': 612,
            }
        },
    ]

returns:
    None
"""
def load_measurements(data):
    logger.debug("loading measurements from {} sensors".format(len(data)))

    for d in data:
        meas = None
        sensor = get_or_create_sensor(d)
        if not sensor:
            continue

        for k, v in d['measurements'].items():
            params = {
                'sensor_id': sensor.id,
                'value': v,
                'type': k,
                'created': g_utcnow }

            try:
                meas = Measurement(**params)
                db_session.add(meas)
                db_session.commit()
            except Exception:
                logger.exception("create new Measurement failed")
                continue

            # sensors not assigned to a room cannot have actions. so skip
            if sensor.room_id is None:
                continue

            room = Room.query.get(sensor.room_id)
            if not room:
                continue

            for action in room.actions:
                if meas.type == action.measurement_type and (
                    action.sensor == 'any' or int(action.sensor) == sensor.id):
                    handle_action(action, meas)
                else:
                    continue


"""
Handle an Action and Measurement for necessary... actions.

Pre-filtering has already been done in load_measurements(), to ensure these
two objects are related and compatible.

params:
    - an Action object
    - a Measurement object
return:

"""
def handle_action(action, meas):
    logger.debug("handling action {}".format(action))
    logger.debug("action data: {}".format(action.data))
    data = json.loads(action.data)
    cls = data.pop('class')

    # create instance of the action plugin that will process this info
    plugin = rehydrate_plugin_instance(ActionPluginBase, cls, data)
    plugin.handle_measurement(action, meas)

    return


"""
Process any pending FutureAction events
"""
def handle_future_actions():
    logger.debug("processing future outlet actions")
    oc = None
    changes = 0
    actions = FutureOutletAction.query.filter(
                FutureOutletAction.run_at <= g_utcnow).filter(
                FutureOutletAction.completed == None).all()

    if actions:
        oc = OutletController()

    for a in actions:
        outlet = json.loads(a.outlet)
        if a.action == 'on':
            if oc.turn_on(outlet):
                a.completed = g_utcnow
                changes += 1

        elif a.action == 'off':
            if oc.turn_off(outlet):
                a.completed = g_utcnow
                changes += 1

    if changes > 0:
        db_session.commit()


# ############################################################################

if __name__ == '__main__':
    # global datetimes
    g_now = datetime.datetime.now().replace(second=0, microsecond=0)
    g_utcnow = datetime.datetime.utcnow().replace(second=0, microsecond=0)

    # init logging
    logger = logging.getLogger('potnanny')
    logger_format = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')

    # handle args
    parser = argparse.ArgumentParser(description='Potnanny measurement polling script')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-e','--environment', default='production')
    parser.add_argument('-f','--force', action='store_true')
    args = parser.parse_args()

    # config app environment
    app_config = None
    if args.environment == 'production':
        app_config = Production
    elif args.environment == 'testing':
        app_config = Testing
    elif args.environment == 'development':
        app_config = Development
    else:
        raise RuntimeError("Must provide config environment")

    # init database
    init_engine(app_config.SQLALCHEMY_DATABASE_URI)
    init_db()

    # fine tune the logging
    if args.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logger_format)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    else:
        handler = logging.FileHandler(os.path.join(
            app_config.POTNANNY_LOG_PATH, 'poll.log'))
        handler.setFormatter(logger_format)
        logger.setLevel(logging.WARNING)
        logger.addHandler(handler)

    # Handle any FutureAction events first.
    handle_future_actions()

    # get poll interval settings from db
    pollcfg = PollSetting.query.first()
    if not pollcfg:
        pollcfg = PollSetting()
        db_session.add(pollcfg)
        db_session.commit()

    # run collection and actions now?
    if not args.force and g_now.minute % pollcfg.interval > 0:
        logger.debug("incorrect interval. nothing to do right now")
        sys.exit(0)

    main()
