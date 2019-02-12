from potnanny.extensions import db
from sqlalchemy import func


class PollSetting(db.Model):
    __tablename__ = 'poll_settings'

    id = db.Column(db.Integer, primary_key=True)
    interval = db.Column(db.Integer, nullable=False, default=5)
    created = db.Column(db.DateTime, default=func.now())
