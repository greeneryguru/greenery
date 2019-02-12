from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from sqlalchemy.orm import relationship
from potnanny.core.database import Base
from potnanny.core.models.measurement import Measurement


class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    name = Column(String(48), default='my sensor')
    address = Column(String(48), unique=True, nullable=False)
    model = Column(String(48), nullable=True)
    created = Column(DateTime, default=func.now())

    # relationships
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=True)

    def __repr__(self):
        return "<Sensor({})>".format(self.name)


    """
    Get all the latest measurement values from this sensor

    params:
        None
    returns:
        a dict
    """
    def latest_readings(self):
        results = db_session.query(
            Measurement.type, Measurement.value, func.max(Measurement.created)
            ).filter(Measurement.sensor_id == self.id).order_by(
            Measurement.created.desc(), Measurement.type).group_by(
            Measurement.type).all()

        if not results:
            return {}

        return {r[0]:r[1] for r in results}

    """
    get list of all valid measurement types for this sensor type, based what it
    has reported in the past.

    params:
        None
    returns:
        a list ['battery','temperature','humidity']
    """
    def measurement_types(self):
        results = db_session.query(Measurement.type).filter(
            Measurement.sensor_id == self.id).order_by(
            Measurement.type).group_by(
            Measurement.type).all()

        if not results:
            return []

        return [r[0] for r in results]
