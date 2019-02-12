import datetime
from flask import Blueprint, render_template, redirect, request, url_for, abort, jsonify
from potnanny.extensions import db
from .controller import graph_data


view = Blueprint('measurement', __name__,
                    template_folder='templates', url_prefix='/measurements')


@view.route('/graph', methods=['GET'])
def simple_graph():
    sensors = request.args.get('sensors')
    measurements = request.args.get('measurements')
    hours = request.args.get('hours', None)
    start = request.args.get('start', None)
    end = request.args.get('start', None)
    anno = request.args.get('annotations', False)

    if not sensors:
        return None

    sensors = [int(n) for n in sensors.split(',')]
    if measurements:
        measurements = [n for n in measurements.split(',')]

    if hours:
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(hours=int(hours))

    chart_args = {
        'dates_on': request.args.get('dates_on', True),
        'legend_on': request.args.get('legend_on', False),
        'convert_c': False,
        'annotations': anno,
    }

    data = graph_data(sensors, measurements, start, end, **chart_args)
    return jsonify(data)
