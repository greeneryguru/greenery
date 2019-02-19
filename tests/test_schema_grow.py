#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
from potnanny.apps.grow.schemas import GrowSchema


class TestModels(unittest.TestCase):
# ###############################################

    # basic test
    def test_init(self):
        data, errors = GrowSchema().load(
            {"name": "test grow 1", "room_id": 1}
        )
        assert len(errors) == 0
        assert "name" in data


    # feed some invalid fields to the schema, it should skip them
    def test_id_init(self):
        data, errors = GrowSchema().load(
            {"name": "test grow 2", "room_id": 1, "id": 2}
        )
        assert len(errors) == 0
        assert "name" in data
        assert "id" not in data


    # feed some invalid fields to the schema, it should skip them
    def test_bad_init(self):
        data, errors = GrowSchema().load(
            {"name": "test grow 3", "room_id": 1, "foo": "bar"}
        )
        assert len(errors.items()) == 0
        assert "name" in data
        assert "id" not in data
        assert "foo" not in data

    # feed some invalid fieldtypes. should fail to pass schema
    def test_bad_type(self):
        data, errors = GrowSchema().load(
            {"name": 3, "room_id": 1}
        )
        assert "name" in errors

if __name__ == '__main__':
    unittest.main()
