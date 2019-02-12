#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from potnanny.config import Testing
from potnanny.core.database import db_session, init_db, init_engine
from potnanny.core.models import Action
# from potnanny.core.schemas import ActionSchema


class TestModel(unittest.TestCase):
# ###############################################

    def setUp(self):
        init_engine(Testing.SQLALCHEMY_DATABASE_URI)
        init_db()


    def tearDown(self):
        db_session.remove()


    # room
    # ---------------------------------
    def test_init(self):
        data = {
            'name': 'test action',
            'meas_type': 'temperature',
            'sensor': '1',
            'room_id': 1,
            'sleep_minutes': 15,
            'data': json.dumps({
                'on_condition': 'gt',
                'on_value': 80,
                'off_condition': 'lt',
                'off_value': 75,
                'outlet': {
                    'name': "test outlet",
                    'id': "1",
                    'type': "wireless"
                },
            }),
        }

        obj = Action(**data)
        db_session.add(obj)
        db_session.commit()

        assert obj.id is not None
        assert obj.name == 'test action'
        assert obj.is_active is True
        assert obj.created is not None
        # serialized, errors = ActionSchema().dump(obj)
        # assert not errors



if __name__ == '__main__':
    unittest.main()
