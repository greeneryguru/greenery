#!/usr/bin/env python3

import os
import unittest
import json
from flask import current_app
from potnanny import create_app
from potnanny.config import Testing
from potnanny.extensions import db
from potnanny.core.models import Grow
from potnanny.core.schemas import GrowSchema


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
        obj = Grow(name='test grow', room_id=1)
        db.session.add(obj)
        db.session.commit()

        assert obj.id is not None
        assert obj.name == 'test grow'
        assert obj.started is not None
        assert obj.ended is None

        data, errors = GrowSchema().dumps(obj)
        assert not errors

if __name__ == '__main__':
    unittest.main()
