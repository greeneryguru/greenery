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
                'display': False
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

class ChartColor(object):
    COLORS = [
        "rgb(255, 193, 7)",
        "rgb(104, 159, 56)",
        "rgb(139, 195, 74)",
        "rgb(33, 33, 33)",
        "rgb(220, 180, 130)",
    ]

    @classmethod
    def index_color(cls, index):
        return cls.COLORS[index % len(cls.COLORS)]
