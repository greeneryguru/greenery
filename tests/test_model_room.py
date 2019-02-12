#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
from potnanny import create_app
from potnanny.config import Testing
from potnanny.core.database import db_session, init_db, init_engine
from potnanny.core.models import Room
from potnanny.core.schemas import RoomSchema
# from potnanny.core.schemas import ActionSchema


class TestModel(unittest.TestCase):
# ###############################################

    def setUp(self):
        init_engine(Testing.SQLALCHEMY_DATABASE_URI)
        init_db()


    def tearDown(self):
        db_session.remove()


    def test_init(self):
        r = Room(name='test room')
        db_session.add(r)
        db_session.commit()

        assert r.id is not None
        assert r.name == 'test room'
        assert r.created is not None

        data, errors = RoomSchema().dump(r)
        assert not errors

if __name__ == '__main__':
    unittest.main()
