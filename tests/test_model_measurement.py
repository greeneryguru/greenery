#!/usr/bin/env python3

import os
import unittest
import json
from potnanny import create_app
from potnanny.config import Testing
from potnanny.extensions import db
from potnanny.apps.core.models import MeasurementTypeMap, Measurement


class TestModels(unittest.TestCase):
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


    def test_create(self):
        m = Measurement(
            mtype='tc',
            value=21.0,
            sensor_id=1
        )
        db.session.add(m)
        db.session.commit()

        assert m.id is not None
        assert m.value == 21.0


if __name__ == '__main__':
    unittest.main()
