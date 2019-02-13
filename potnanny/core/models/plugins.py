class ActionPluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class BlePluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class ActionPluginBase(object, metaclass=ActionPluginMount):
    pass

class BlePluginBase(object, metaclass=BlePluginMount):
    pass
