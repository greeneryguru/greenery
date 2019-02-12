#!/usr/bin/env python3

import os
import unittest
import json
from flask import current_app
from potnanny import create_app
from potnanny.config import Testing
from potnanny.extensions import db
from potnanny.core.models import Error
from potnanny.core.schemas import ErrorSchema


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
        obj = Error(
            title='test error',
            message='foo bar'
        )
        db.session.add(obj)
        db.session.commit()

        assert obj.id is not None
        assert obj.title == 'test error'
        assert obj.created is not None

        data, errors = ErrorSchema().dumps(obj)
        assert not errors


if __name__ == '__main__':
    unittest.main()
