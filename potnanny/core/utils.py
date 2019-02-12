import os
import re
import copy
import datetime
import subprocess
import logging
import unicodedata
from importlib.machinery import SourceFileLoader
from potnanny.core.models.plugins import ActionPluginBase

logger = logging.getLogger(__name__)


"""
Reduce a float to only 1 decimal place

params:
    a float
returns:
    a float
"""
def reduce_float(f):
    return float("%0.1f" % f)


"""
convert celsius to fahrenheit

params:
    a number
    reduce/round floats to only 1 decimal place? True (default)|False

returns:
    a float
"""
def convert_celsius(val, reduce=True):
    f = float(val) * 1.8 + 32
    if reduce:
        return reduce_float(f)
    else:
        return f


"""
convert a datetime object to format that javascript can handle
"""
def datetime_handler(obj):

    if hasattr(obj, 'isoformat'):
        obj = obj.replace(tzinfo=datetime.timezone.utc)
        return obj.isoformat()
    else:
        raise TypeError("Invalid Object '{}''. Expected a datetime".format(type(obj)))


"""
rehydrate an instance of a plugin based on JSON data

as I document this, I wonder if it might be better to pickle the objects and
store them in the db that way? I will consider this...

params:
    - the parent class the child instance inherits from. Usually, either
      ActionPluginBase or BlePluginBase.
    - the class name of the child we are rehydrating
    - init options for the child instance

returns:
    an instance of a class, or None if instance could not be created.
"""
def rehydrate_plugin_instance(parent_class, class_name, options):
    for plugin in parent_class.plugins:
        if plugin.__name__ == class_name:
            obj = plugin(**options)
            return obj

    return None


"""
run a system command as a subprocess

params:
    - a list of commands, like ['ls','-la']
    - shell, True|False (default) If shell is set to true, the command list will
      be flattened to a single string
returns:
    tuple (exit-code, stdout, stderr)
"""
def subprocess_command(cmd, shell=False):
    if shell and type(cmd) is list:
        cmd = " ".join(cmd)

    child = subprocess.Popen(cmd, shell=shell,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, errors = child.communicate()
    return (child.returncode, output, errors)


"""
Load any plugin files from the named path.

Yes, arbitrarily loading source files found lying around in the filesystem is
a risky thing. But, our ecosystem is quite closed so, -meh-

params:
    a folder path
returns:
    None
"""
def load_plugins(path):
    if not path:
        raise ValueError("path required for plugin loader")

    if not os.path.exists(path):
        raise RuntimeError("path {} not found".format(path))

    files = [f for f in os.listdir(path)
                if f.endswith('.py') and f not in ['__init__.py']]

    for f in files:
        mod = f.split(".")[0]
        fname = os.path.join(path, f)
        try:
            result = SourceFileLoader(mod, fname).load_module()
        except Exception:
            logger.exception("failed to load '{}'".format(fname))

    return


"""
Scan for all BLE devices.

params:
    None

returns:
    a list of dicts, like: [{'name': NAME, 'address': ADDRESS}, ]
"""
def blescan_devices():
    logger.debug("scanning BLE devices")
    command = ['sudo', 'blescan']
    rval, output, errors = subprocess_command(command, False)
    if not rval:
        buf = clean_blescan_output(output)
        return parse_blescan_buffer(buf)
    else:
        logger.warning("blescan_devices(): {}".format(errors))
        return None


"""
Clean escape chars and hex chars from the output of the blescan cmd.

params:
    a block of binary-like text

return:
    a list of clean lines
"""
def clean_blescan_output(buf):
    results = []
    for line in buf.splitlines():
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        clean = line.decode("utf-8")
        clean = ansi_escape.sub('', clean)
        results.append(clean)

    return results


"""
parse the blescan stdout buffer and extract valid device names/addresses

params:
    a list of *sanitized* lines from the output of the blescan command.

returns:
    a list of dicts like [{'address': ADDRESS, 'name': NAME}, ]
"""
def parse_blescan_buffer(data):
    devices = []
    buf = {}
    for line in data:
        if re.search(r'^\s*Device', line):
            if buf:
                devices.append(copy.deepcopy(buf))
                buf = {}

            match = re.search(r'(?P<address>\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', line)
            if match:
                buf['address'] = match.group('address')
                continue

        match = re.search(r"^\s*Complete Local Name: '(?P<name>.+)'", line)
        if match:
            buf['name'] = match.group('name')

    # one last check of the buffer
    if buf:
        devices.append(copy.deepcopy(buf))

    return devices


"""
evaluate a conditional str statement against a value. like; (22, "value gt 80")

params:
    - a value (float)
    - a string statement, like "value lt 100"

returns:
    True|False
"""
def eval_condition(val, stmt):
    atoms = re.split(r'\s+', stmt)
    if atoms[0] == 'value':
        atoms = atoms[1:]

    oper, threshold = atoms

    if oper == 'lt' and val < threshold:
        return True
    elif oper == 'le' and val <= threshold:
        return True
    elif oper == 'gt' and val > threshold:
        return True
    elif oper == 'ge' and val >= threshold:
        return True
    elif oper == 'eq' and val == threshold:
        return True
    elif oper == 'ne' and val != threshold:
        return True

    return False
