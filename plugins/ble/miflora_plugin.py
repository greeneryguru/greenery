import re
import logging

from potnanny.core.models import BlePluginBase
from btlewrap.bluepy import BluepyBackend

import miflora
from miflora.miflora_poller import MiFloraPoller

logger = logging.getLogger('potnanny.plugin')


"""
Potnanny Plugin for the Xiaomi Mi Flower Care soil sensor
"""
class MifloraPlugin(BlePluginBase):

    """
    devices is a list like [{'name': NAME, 'address': ADDRESS}, ]
    """
    @classmethod
    def poll(cls, devices):
        measurements = []
        regex = re.compile(r'flower\s+(care|mate)', re.IGNORECASE)
        for device in devices:
            if 'name' not in device:
                continue

            # filter out any names that don't match our regex
            if not re.search(regex, device['name']):
                continue

            # poll our device
            logger.debug("polling device {}".format(device))

            result = cls.poll_device(device)
            logger.debug("result: {}".format(result))
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
            'temperature': miflora.miflora_poller.MI_TEMPERATURE,
            'soil-moisture': miflora.miflora_poller.MI_MOISTURE,
            'light': miflora.miflora_poller.MI_LIGHT,
            'soil-ec': miflora.miflora_poller.MI_CONDUCTIVITY,
            'battery': miflora.miflora_poller.MI_BATTERY,
        }

        try:
            poller = MiFloraPoller(device['address'], BluepyBackend)
            for key, code in readings.items():
                value = poller.parameter_value(code)
                if value is not None:
                    data['measurements'][key] = value
        except Exception:
            logger.exception("Failed to poll device {}".format(device))

        if len(data['measurements']):
            return data
        else:
            return None
