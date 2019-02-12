from sqlalchemy import (Column, Integer, String, Text, Boolean, Float,
        DateTime, ForeignKey, func)
from potnanny.core.database import Base


class PollSetting(Base):
    __tablename__ = 'poll_settings'

    id = Column(Integer, primary_key=True)
    interval = Column(Integer, nullable=False, default=5)
    created = Column(DateTime, default=func.now())
