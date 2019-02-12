#!/usr/bin/env python3

"""

create 8 hours of test measurements for a dummy sensor

"""


import os
import sys
import re
import datetime
import argparse
import random

from potnanny.config import Production, Development, Testing
from potnanny.core.database import init_db, db_session
from potnanny.core.models import MeasurementTypeMap, Measurement, Sensor, \
        Room

def main():
    # a test room
    r = Room.query.filter_by(name='test room').first()
    if not r:
        r = Room(name='test room')
        db.session.add(r)
        db.session.commit()

    # a test sensor
    s = Sensor.query.filter_by(name='test sensor', address='11:22:33:44:55').first()
    if not s:
        s = Sensor(
            name='test sensor',
            model='foo brand',
            address='11:22:33:44:55',
            room_id=r.id
            )
        db.session.add(s)
        db.session.commit()

    end = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    now = end - datetime.timedelta(hours=args.hours)
    codes = [MeasurementTypeMap().lookup_code(n) for n in ['temperature','humidity','soil-moisture']]

    while now <= end:
        for code in codes:
            value = 0
            if code == 2:
                value=random.randint(20,28)

            if code == 3:
                value=random.randint(40,60)

            if code == 6:
                value=random.randint(18,24)

            m = Measurement(
                code=code,
                value=value,
                sensor_id=s.id,
                created=now
            )
            db.session.add(m)

        db.session.commit()
        now = now + datetime.timedelta(minutes=5)


# ############################################################################

if __name__ == '__main__':
    config = None
    now = datetime.datetime.now().replace(second=0, microsecond=0)

    parser = argparse.ArgumentParser(description='create some fake measurement data.')
    parser.add_argument('-e', '--environment',
                            choices=['production','development','testing'],
                            default='production')
    parser.add_argument('--hours', type=int, default=8)

    args = parser.parse_args()

    if args.environment == 'development':
        config = Development
    elif args.environment == 'testing':
        config = Testing
    elif args.environment == 'production':
        config = Production

    init_db(config.SQLALCHEMY_DATABASE_URI)
    main()
