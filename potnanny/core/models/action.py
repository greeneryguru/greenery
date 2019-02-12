from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from sqlalchemy.orm import relationship
from potnanny.core.database import Base

"""
an Action is a layout for something that should happen, based on a measurement
type from one, or any, sensor in a room.

The 'data' is json text, which will be used to rehydrate an object. i.e.,
    data = {
        'class': 'TriggeredOnOffAction',
        'on_condition': 'value gt 80',
        'off_condition': 'value lt 75',
        'outlet': {
            'name': "test outlet",
            'id': "1",
            'type': "wireless" },
    }

"""
class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    name = Column(String(48), default='my action')
    measurement_type = Column(String(24), nullable=False)
    sensor = Column(String(16), nullable=False, default="any")
    is_active = Column(Boolean, default=True)
    data = Column(Text, nullable=False)
    sleep_minutes = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, default=func.now())

    # relationships
    room_id = Column(Integer, ForeignKey('rooms.id'))

    # An action may have "None" or "One" open triggers at any given time.
    # There should never be more than one, but a list is always returned
    triggers = relationship('Trigger',
        primaryjoin="and_( Action.id==Trigger.action_id, or_(Trigger.closed == None, Trigger.closed > func.now()) )",
        backref='action',
        lazy=True,
        cascade='all,delete')


    def __repr__(self):
        return "<Action({})>".format(self.name)
