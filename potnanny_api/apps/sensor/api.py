from flask import Blueprint, request, url_for, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.models.sensor import Sensor
from potnanny_core.schemas.sensor import SensorSchema
from potnanny_core.database import db_session
from potnanny_api.crud import CrudInterface
from potnanny_core.models.measurement import Measurement
from potnanny_core.utils import datetime_for_js, convert_celsius
from potnanny_core.models.setting import TemperatureDisplay
from potnanny_api.chart_utils import ChartColor, CHARTBASE

bp = Blueprint('sensor_api', __name__, url_prefix='/api/1.0/sensors')
api = Api(bp)
ifc = CrudInterface(db_session, Sensor, SensorSchema)

class SensorListApi(Resource):

    @jwt_required
    def get(self):
        ser, err, code = ifc.get()
        if err:
            return err, code

        return ser, code

    @jwt_required
    def post(self):
        data, errors = SensorSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.create(data)
        if err:
            return err, code

        return ser, code


class SensorApi(Resource):

    @jwt_required
    def get(self, pk):
        ser, err, code = ifc.get(pk)
        if err:
            return err, code

        return ser, code

    @jwt_required
    def put(self, pk):
        data, errors = SensorSchema().load(request.get_json())
        if errors:
            return errors, 400

        ser, err, code = ifc.edit(pk, data)
        if err:
            return err, code

        return ser, code

    @jwt_required
    def delete(self, pk):
        ser, err, code = ifc.delete(pk)
        if err:
            return err, code

        return ser, code


class SensorChartApi(Resource):

    @jwt_required
    def get(self, pk, prev_hours=12):
        """Query measurements for graphing functions."""

        # so. much. painful. work. to. build. charts. ug!
        chart_tracker = {}
        chart = copy.deepcopy(CHARTBASE)
        temp_setting = TemperatureDisplay.get()
        now = datetime.datetime.utcnow()

        start = request.args.get('start', None)
        end = request.args.get('start', None)

        if start is None:
            start = now - datetime.timedelta(hours=prev_hours)

        if end is None:
            end = now

        sensor = Sensor.query.get(pk)
        if not sensor:
            return {'message': "Sensor with id '{}' not found".format(pk)}, 404

        types = sensor.measurement_types()
        try:
            types.remove('battery')
        except:
            pass

        # track which index/data group this measurement type is stored in
        for t in types:
            if t not in chart_tracker:
                chart_tracker[t] = len(chart_tracker)
                chart['data']['datasets'].append({})

        # finally. get some results
        results = Measurement.query.filter(
            Measurement.sensor_id == sensor.id).filter(
            Measurement.type.in_(types)).and_(
            Measurement.created >= start, Measurement.created <= end).order_by(
            Measurement.created.asc()).all()

        for r in results:
            tstamp = datetime_for_js(r.created)
            if tstamp not in chart['data']['labels']:
                chart['data']['labels'].append(tstamp)

            value = r.value
            if r.type == 'temperature' and temp_setting == 'fahrenheit':
                value = convert_celsius(value)

            if 'data' not in chart['data']['datasets'][chart_tracker[r.type]]:
                chart['data']['datasets'][chart_tracker[r.type]] = {
                    'label': r.type,
                    'data': [],
                    'fill': 'false',
                    'lineTension': 0.3,
                    'borderColor': ChartColor.index_color(chart_tracker[r.type]),
                }

            chart['data']['datasets'][chart_tracker[r.type]]['data'].append(value)

        chart['options']['legend']['display'] = True
        chart['options']['scales']['xAxes'][0]['display'] = True

    return chart, 200


api.add_resource(SensorListApi, '')
api.add_resource(SensorApi, '/<int:pk>')
api.add_resource(SensorChartApi, '/<int:pk>/chart')
