#!/usr/bin/env python3

import os
import unittest
import json
import datetime
import random
from potnanny.core.schemas import (WirelessOutletSchema, GenericOutletSchema,
    VesyncOutletSchema)


class TestGenericOutlet(unittest.TestCase):
# ###############################################

    # basic test of GenericOutletSchema
    def test_basic(self):
        data, errors = GenericOutletSchema().load({
            "name": "test outlet",
            "id": "1234-1234-1234",
            "type": "wifi-switch"
        })
        assert len(errors) == 0
        assert "name" in data

    # Check that the  GenericOutletSchema can properly transpose
    # vesync "deviceName" to "name"
    def test_transpose(self):
        data, errors = GenericOutletSchema().load({
            "deviceName": "test outlet",
            "id": "1234-1234-1234",
            "type": "wifi-switch"
        })
        assert len(errors) == 0
        assert "name" in data



class TestWirelessOutlet(unittest.TestCase):
# ###############################################

    # basic test of WirelessOutletSchema
    def test_rf_init(self):
        data, errors = WirelessOutletSchema().load({
            "name": "test grow 1",
            "on_code": "12345 1 24",
            "off_code": "12346 1 24",
        })
        assert len(errors) == 0
        assert "name" in data


    # feed some invalid fields to the schema, it should skip them
    def test_id_init(self):
        data, errors = WirelessOutletSchema().load({
            "name": "test grow 1",
            "on_code": "12345 1 24",
            "off_code": "12346 1 24",
            "foo": "bar",
        })
        assert len(errors) == 0
        assert "name" in data
        assert "foo" not in data


    # feed some invalid fields to the schema, it should skip them
    def test_bad_init(self):
        data, errors = WirelessOutletSchema().load({
            "name": "test grow 1",
            "on_code": "12345 1 24",
            "off_code": "12346 1 24",
            "foo": "bar",
            "id": 1,
        })
        assert len(errors.items()) == 0
        assert "name" in data
        assert "id" not in data
        assert "foo" not in data


    # feed some invalid fieldtypes. should fail to pass schema
    def test_bad_type(self):
        data, errors = WirelessOutletSchema().load(
            {"name": 3, "room_id": 1}
        )
        assert "name" in errors


class TestVesyncOutlet(unittest.TestCase):
# ###############################################

    def test_vs_init(self):
        data, errors = VesyncOutletSchema().load({
            "name": "test grow 1",
            "type": "wifi-switch",
            "relay": "break",
            "status": "online",
        })
        print(data)
        assert len(errors) == 0
        assert "name" in data


if __name__ == '__main__':
    unittest.main()
