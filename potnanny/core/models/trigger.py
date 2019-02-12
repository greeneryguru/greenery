from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from potnanny.core.database import Base


class Trigger(Base):
    __tablename__ = 'triggers'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    closed = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # relationships
    action_id = Column(Integer, ForeignKey('actions.id'))

    def __repr__(self):
        return "<Trigger(created={},action={})>".format(
            self.created,
            self.action_id)
