#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
import copy
from potnanny.core.schemas import ActionSchema

base = {
    "name": "test control",
    "sleep_minutes": 60,
    "is_active": True,
    "sensor": "any",
    "measurement_type": "temperature",
    "data": json.dumps({
        "class": "TriggeredOnOffAction",
        "name": "outlet on/off",
        "on_condition": "value gt 80",
        "off_condition": "value lt 76",
        "outlet": {
            "id": "1",
            "name": "test outlet",
            "type": "wireless"
        }
    }),
    "triggers": [{
        "id": 1,
        "created": "1999-01-01",
        "closed": "1999-01-03",
        "measurement_id": 1
    }]
}


class TestModels(unittest.TestCase):
# ###############################################
    # basic test
    def test_action(self):
        # make copy of base data for testing
        cp = copy.deepcopy(base)

        data, errors = ActionSchema().load(cp)
        assert "name" in data


    # test ActionSchema with bogus data
    def test_missing_val_01(self):

        # duplicate, and corrupt data
        cp = copy.deepcopy(base)
        del cp['sensor']

        data, errors = ActionSchema().load(cp)
        assert 'sensor' in errors


    # test ActionSchema with bogus data
    def test_missing_val_02(self):

        # duplicate, and corrupt data
        cp = copy.deepcopy(base)
        del cp['measurement_type']

        data, errors = ActionSchema().load(cp)
        assert 'measurement_type' in errors


if __name__ == '__main__':
    unittest.main()
