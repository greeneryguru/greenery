#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
from potnanny.apps.sensor.schemas import SensorSchema


class TestModels(unittest.TestCase):
# ###############################################

    # basic test
    def test_sensor(self):
        data, errors = SensorSchema().load({"name": "test sensor 1"})
        assert len(errors.items()) == 0
        assert "name" in data


    # feed some dump-only fields into serializer. should skip them
    def test_forbidden_sensor(self):
        data, errors = SensorSchema().load({
            "name": "test sensor 1",
            "address": "11:22:33:44:55:66",
            "model": "test soil sensor"}
        )
        assert len(errors.items()) == 0
        assert "name" in data
        assert "address" not in data
        assert "model" not in data


if __name__ == '__main__':
    unittest.main()
