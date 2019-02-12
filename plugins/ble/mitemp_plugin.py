import re

from potnanny.core.models import BlePluginBase
from btlewrap.bluepy import BluepyBackend

import mitemp_bt
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller


"""
Potnanny Plugin for the Xiaomi Mi BT temp/humidity sensor
"""
class MiTempHumidityPlugin(BlePluginBase):

    """
    devices is a list like [(device-address, device-name), ]
    """
    @classmethod
    def poll(cls, devices):
        measurements = []
        regex = re.compile(r'MJ_HT_V\d+', re.IGNORECASE)
        for device in devices:
            if 'name' not in device:
                continue

            # filter out any names that don't match our regex
            if not re.search(regex, device['name']):
                continue

            # poll our device
            result = cls.poll_device(device)
            if result:
                measurements.append(result)

        if not len(measurements):
            return None

        return measurements


    @classmethod
    def poll_device(cls, device):
        data = {
            'name': device['name'],
            'address': device['address'],
            'measurements': {},
        }

        readings = {
            'temperature': mitemp_bt.mitemp_bt_poller.MI_TEMPERATURE,
            'humidity': mitemp_bt.mitemp_bt_poller.MI_HUMIDITY,
            'battery': mitemp_bt.mitemp_bt_poller.MI_BATTERY
        }

        try:
            poller = MiTempBtPoller(device[0], BluepyBackend)
            for key, code in readings.items():
                value = poller.parameter_value(code)
                if value is not None:
                    data['measurements'][key] = value
        except:
            pass

        if len(data['measurements']):
            return data
        else:
            return None
