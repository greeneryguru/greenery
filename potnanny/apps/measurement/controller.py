import copy
import datetime
from potnanny.core.models import Measurement, MeasurementTypeMap, Sensor
from potnanny.extensions import db
from potnanny.core.schemas import ActionSchema
from .models import ChartBuilder


"""

params:
    - a list of sensor ids to collect from.
    - a measurement type name to collect.
    - start datetime
    - end datetime

    - keyword args to be passed to ChartBuilder object:
        legend_on   = True|False,
        dates_on    = True|False,
        colors      = [list of custom RBG color codes],
        convert_c   = True|False, (convert celsius to fahrenheit)
        show_triggers = False

"""
def graph_data(sensors, measurements, start=None, end=None, **kwargs):
    default_hours = 4
    index_tracker = {}
    sensor_tracker= {}
    cb = ChartBuilder(**kwargs)

    if type(sensors) is int:
        sensors = [sensors]
    elif type(sensors) is list:
        sensors = [int(n) for n in sensors]
    else:
        raise ValueError("sensors must be int or list of ints")

    if type(measurements) is not list:
        measurements = [measurements]

    # translate measurements from the common name, to the code number
    measurements = [MeasurementTypeMap().lookup_code(n) for n in measurements]

    if not end:
        end = datetime.datetime.utcnow()

    if not start:
        start = end - datetime.timedelta(hours=default_hours)

    results = Measurement.query.filter(
            Measurement.sensor_id.in_(sensors)).filter(
            Measurement.code.in_(measurements)).filter(
            Measurement.created >= start).filter(
            Measurement.created <= end).order_by(
            Measurement.created).all()

    if not results:
        return None

    for m in results:
        if m.sensor_id not in sensor_tracker:
            s = Sensor.query.get(m.sensor_id)
            sensor_tracker[m.sensor_id] = s

        slug = "{}".format(MeasurementTypeMap().lookup_name(m.code))

        if slug not in index_tracker:
            index_tracker[slug] = len(index_tracker)

        cb.append_datetime_label(m.created)
        if cb.data_index_exists(index_tracker[slug], slug):
            cb.append_value_to_dataset(m.value, index_tracker[slug],
                    MeasurementTypeMap().lookup_name(m.code))


    # add trigger annotations for the chart
    """
    for s in sensors:
        if s.room_id is None:
            continue

        for a in s.room.actions:
            action, errors = ActionSchema().dumps(a)
            if errors:
                continue

            if action['details']['sensor'] == 'any' or \
                action['details']['sensor'] == s.id:

                for t in action.triggers:
                    if t.measurement.code not in codes:
                        continue

                    cb.add_annotation({
                        'value': t.created,
                        'label': a.name,
                    })
    """

    return cb.results()
