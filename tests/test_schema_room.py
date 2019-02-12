#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
from potnanny.core.schemas import RoomSchema


class TestModels(unittest.TestCase):
# ###############################################

    # basic test
    def test_room(self):
        data, errors = RoomSchema().load(
            {"name": "test room 1"}
        )
        assert len(errors.items()) == 0
        assert "name" in data


    # feed some invalid fields to the schema, it should skip them
    def test_id_room(self):
        data, errors = RoomSchema().load(
            {"name": "test room 2", "id": "1"}
        )
        assert len(errors.items()) == 0
        assert "name" in data
        assert "id" not in data


    # feed some invalid fields to the schema, it should skip them
    def test_bad_room(self):
        data, errors = RoomSchema().load(
            {"name": "test room 3", "id": "1", "foo": "bar"}
        )
        assert len(errors.items()) == 0
        assert "name" in data
        assert "id" not in data
        assert "foo" not in data

if __name__ == '__main__':
    unittest.main()
