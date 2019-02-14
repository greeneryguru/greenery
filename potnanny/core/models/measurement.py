from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from potnanny.core.database import Base


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    type = Column(String(24), nullable=False, index=True, default='battery')
    value = Column(Float, default=0.0)
    created = Column(DateTime, default=func.now())

    # relationships
    sensor_id = Column(Integer, ForeignKey('sensors.id'))

    def __repr__(self):
        return "<Measurement(id={},type={},value={})>".format(
            self.id,
            self.type,
            self.value)