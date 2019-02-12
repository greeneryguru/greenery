#!/usr/bin/env python3

import os
import unittest
import json
import re
from potnanny import create_app
from potnanny.config import Testing
from potnanny.extensions import db
from potnanny.apps.user.models import User


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

    # user
    # ---------------------------------
    def test_user(self):
        u = User(userid='test-user')
        db.session.add(u)
        db.session.commit()

        assert u.id is not None
        assert u.email_confirmed is None
        assert u.show_fahrenheit is False

if __name__ == '__main__':
    unittest.main()
