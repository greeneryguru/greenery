from flask import Flask, current_app, jsonify
from .config import BaseConfig, Development, Production, Testing
from .extensions import jwt
from potnanny_core.database import init_engine, init_db, init_users


__all__ = ['create_app']


def create_app(config=Development):
    app = Flask(config.PROJECT)

    app.config.from_object(config)
    with app.app_context():
        config_database(app)
        config_api(app)
        config_extensions(app)

    return app

def config_database(app):
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    init_db()
    init_users()

def config_extensions(app):
    jwt.init_app(app)

def config_api(app):
    from potnanny_api.apps.auth.api import bp as auth_bp
    app.register_blueprint(auth_bp)

    from potnanny_api.apps.user.api import bp as user_bp
    app.register_blueprint(user_bp)

    from potnanny_api.apps.room.api import bp as room_bp
    app.register_blueprint(room_bp)

    from potnanny_api.apps.sensor.api import bp as sensor_bp
    app.register_blueprint(sensor_bp)

    from potnanny_api.apps.grow.api import bp as grow_bp
    app.register_blueprint(grow_bp)

    from potnanny_api.apps.action.api import bp as action_bp
    app.register_blueprint(action_bp)

    from potnanny_api.apps.outlet.api import bp as outlet_bp
    app.register_blueprint(outlet_bp)

    from potnanny_api.apps.schedule.api import bp as schedule_bp
    app.register_blueprint(schedule_bp)

    from potnanny_api.apps.plugin.api import bp as plugin_bp
    app.register_blueprint(plugin_bp)
