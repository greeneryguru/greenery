import os
from flask import Blueprint, request, url_for, jsonify, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

from potnanny_core.database import db_session
from potnanny_core.utils import load_plugins
from potnanny_core.models.plugin import ActionPluginBase

bp = Blueprint('plugin_api', __name__, url_prefix='/api/1.0/plugins')
api = Api(bp)

load_plugins(os.path.join(current_app.config['POTNANNY_PLUGIN_PATH'], 'action'))

class ActionPluginListApi(Resource):
    """Class to get ActionPlugin classes."""

    # @jwt_required
    def get(self):
        """Get list of all classes."""
        data = []
        for cls in ActionPluginBase.plugins:
            data.append({
                'class': cls.__name__,
                'name': cls.action_name
            })

        return data, 200

class ActionPluginInterfaceApi(Resource):
    """Class to get interface spec from plugin."""

    # @jwt_required
    def get(self, class_name):
        """Get interface spec."""
        for cls in ActionPluginBase.plugins:
            if cls.__name__ == class_name:
                return cls.interface(), 200

        return {'msg': 'not found'}, 404

api.add_resource(ActionPluginListApi, '/action')
api.add_resource(ActionPluginInterfaceApi, '/action/<class_name>/interface')
