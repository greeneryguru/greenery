from flask import Flask, current_app
from .config import BaseConfig
from .core.database import init_engine, init_db
from .extensions import jwt


__all__ = ['create_app']


def create_app(config=BaseConfig):
    app = Flask(config.PROJECT)

    app.config.from_object(config)
    with app.app_context():
        config_database(app)
        config_extensions(app)
        config_api(app)

    return app


def config_database(app):
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    init_db()


def config_extensions(app):
    jwt.init_app(app)
    # csrf.init_app(app)


def config_api(app):
    pass

    """
    from potnanny.apps.auth import auth_api
    app.register_blueprint(auth_api)

    # from potnanny.apps.auth import auth_view
    # app.register_blueprint(auth_view)

    from potnanny.apps.user import user_api
    app.register_blueprint(user_api)

    from potnanny.apps.dashboard import dash_view
    app.register_blueprint(dash_view)

    from potnanny.apps.room import room_api, room_view
    app.register_blueprint(room_api)
    app.register_blueprint(room_view)

    from potnanny.apps.sensor import sensor_api, sensor_view
    app.register_blueprint(sensor_api)
    app.register_blueprint(sensor_view)

    from potnanny.apps.grow import grow_api, grow_view
    app.register_blueprint(grow_api)
    app.register_blueprint(grow_view)

    from potnanny.apps.action import bp as action
    from potnanny.apps.action import view as action_view
    app.register_blueprint(action)
    app.register_blueprint(action_view)


    from potnanny.apps.rfi import bp as rfi
    app.register_blueprint(rfi)

    from potnanny.apps.outlet import bp as outlet
    app.register_blueprint(outlet)

    from potnanny.apps.pollsetting import bp as pollsetting
    app.register_blueprint(pollsetting)

    from potnanny.apps.measurement import view as meas_view
    app.register_blueprint(meas_view)
    """
