from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from sqlalchemy.orm import relationship
from potnanny.core.database import Base
from potnanny.core.models.measurement import Measurement
from potnanny.core.models.sensor import Sensor


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String(48), unique=True, default='my room')
    notes = Column(Text)
    created = Column(DateTime, default=func.now())

    # relationships #
    sensors = relationship('Sensor', backref='room', lazy=True, cascade='all')
    actions = relationship('Action', backref='room',
                                cascade='all,delete', lazy=True)

    # only active (not ended) grows are linked to the room.
    grows = relationship('Grow',
                primaryjoin="and_(Room.id==Grow.room_id, Grow.ended == None)",
                backref='room',
                cascade='all,delete',
                lazy=True)


    def __repr__(self):
        return "<Room({})>".format(self.name)

    """
    most recent environment values (temperature/humidity).

    params:
        self
    returns:
        a dict, like {'temperature': 20.0, 'humidity': 51}
    """
    def environment(self):
        data = {}
        type_list = ['temperature', 'humidity']
        if self.sensors:
            id_list = [s.id for s in self.sensors]
            for typ in type_list:
                row = Measurement.query.filter(
                        Measurement.type == typ).filter(
                        Measurement.sensor_id.in_(id_list)).order_by(
                        Measurement.created.desc()).first()

                if row:
                    data[typ] = row.value

        return data
