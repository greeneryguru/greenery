from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base


engine = None
db_session = scoped_session(lambda: create_session(bind=engine,
                                                    autocommit=False,
                                                    autoflush=False,))

Base = declarative_base()
Base.query = db_session.query_property()


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)


def init_db():
    from potnanny.core.models import (User, Sensor, Room, Measurement, Grow,
        Action, FutureOutletAction, Trigger, WirelessOutlet, PollSetting,
        OutletSetting)

    Base.metadata.create_all(bind=engine)
