#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
import copy
from from potnanny.apps.outlet.schemas import FutureOutletActionSchema


class TestModels(unittest.TestCase):
# ###############################################
    # basic test
    def test_action(self):
        f = {
            "action": "on",
            "outlet": {
                "id": "1234-1234-1234",
                "type": "wifi-switch",
                "name": "test outlet"
            },
            "run_at": "2019-01-01T18:25:00"
        }

        data, errors = FutureActionSchema().load(f)
        assert not errors


if __name__ == '__main__':
    unittest.main()
