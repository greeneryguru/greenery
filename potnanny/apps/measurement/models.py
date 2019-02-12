import datetime
import copy
import json
from potnanny.core.models import Measurement, MeasurementTypeMap
from potnanny.core.schemas import ActionSchema
from potnanny.extensions import db
from potnanny.core.utils import convert_celsius, datetime_handler


CHARTBASE = {
    'type': 'line',
    'options': {
        'responsive': True,
        'maintainAspectRatio': False,
        'animation': {
            'duration': 0
        },
        'scales': {
            'xAxes': [{
                'display': False,
                'type': 'time',
            }],
            'yAxes': [{
                'ticks': {
                    'beginAtZero': False
                }
            }],
        },
        'legend': {
            'display': False,
            'position': 'bottom',
            'labels': {
                'boxWidth': 8
            }
        }
    },
    'data': {
        'labels': [],
        'datasets': []
    }
}


class ChartBuilder(object):
    def __init__(self, **kwargs):
        self.chart = copy.deepcopy(CHARTBASE)
        self.convert_c = False
        self.legend_on = True
        self.dates_on = True
        self.annotations = False
        self.annotation_color = 'red'
        self.colors = [
            # "rgb(120, 200, 0)",
            # "rgb(20, 140, 220)",
            # "rgb(220, 70, 20)",
            # "rgb(220, 220, 130)",
            # "rgb(220, 180, 130)",
            "rgb(255, 193, 7)",
            "rgb(104, 159, 56)",
            "rgb(139, 195, 74)",
            "rgb(33, 33, 33)",
            "rgb(220, 180, 130)",
        ]

        allowed = ['convert_c', 'legend_on', 'dates_on', 'colors', 'annotations']
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)

        if self.annotations:
            if 'plugins' not in self.chart:
                self.chart['plugins'] = {}

            if 'annotation' not in self.chart['plugins']:
                self.chart['plugins']['annotation'] = {
                    'annotations': []
                }


    """
    Get chart results after all data has been added
    """
    def results(self):
        if self.legend_on:
            self.chart['options']['legend']['display'] = True

        if self.dates_on:
            self.chart['options']['scales']['xAxes'][0]['display'] = True

        return json.dumps(self.chart)


    """
    Get a graph RGB color, based on the index number
    """
    def line_color(self, index):
        return self.colors[index % len(self.colors)]


    """
    accepts a datetime object. converts it to proper json datetime and adds it.
    """
    def append_datetime_label(self, dt):
        label = datetime_handler(dt)
        if label not in self.chart['data']['labels']:
            self.chart['data']['labels'].append(label)


    """
    add a data point to the data block at index N
    """
    def append_value_to_dataset(self, val, idx, typ=None):
        if typ and typ == 'celsius' and self.convert_c:
            val = convert_celsius(val)

        self.chart['data']['datasets'][idx]['data'].append(val)


    """
    add a trigger/annotation to the graph. this creates a vertical line
    indicating an action.
    should contain {'value': n, 'label': l}, where value is the datetime it
    will get drawn to
    """
    def add_annotation(self, data):
        base = {
            'drawTime': 'afterDraw',
			'type': 'line',
			'mode': 'vertical',
			'scaleID': 'x-axis-0',
			'borderWidth': 1,
            'label': 'trigger',
        }

        if not self.annotation:
            return

        if 'value' not in data:
            raise ValueError("must provide annotation value for chart")

        if 'borderColor' not in data:
            base['borderColor'] = self.borderColor

        if type(data['value']) is datetime:
            data['value'] = json.dumps(data['value'], default=date_handler)

        base.update(data)
        self.chart['annotation']['annotations'].append(data)


    """
    check if a dataset exists at particular index.
    if not, create it. requires a label for the dataset
    """
    def data_index_exists(self, idx, label="label"):
        if len(self.chart['data']['datasets']) <= idx or \
            'data' not in self.chart['data']['datasets'][idx]:
            self.chart['data']['datasets'].append({
                'label': label,
                'data': [],
                'fill': 'false',
                'lineTension': 0.3,
                'borderColor': self.line_color(idx),
            })

        return True
