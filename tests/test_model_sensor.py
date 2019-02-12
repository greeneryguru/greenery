#!/usr/bin/env python3

import os
import unittest
import json
import datetime
from potnanny import create_app
from potnanny.config import Testing
from potnanny.extensions import db
from potnanny.core.models import Sensor
from potnanny.core.schemas import SensorSchema


class TestModel(unittest.TestCase):
# ###############################################

    def setUp(self):
        self.app = create_app(Testing)
        self.app.app_context().push()
        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_init(self):
        s = Sensor(
            name='test',
            address='192.168.1.1',
            model='bluetooth sensor'
        )
        db.session.add(s)
        db.session.commit()

        assert s.id is not None
        assert s.name == 'test'
        assert s.address == '192.168.1.1'

        data, errors = SensorSchema().dumps(s)
        assert not errors

if __name__ == '__main__':
    unittest.main()
