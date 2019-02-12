from passlib.hash import pbkdf2_sha256
from potnanny.extensions import db
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(48, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    is_active = db.Column(db.Boolean(), nullable=False, server_default='1')

    def set_password(self, pw):
        self.password = pbkdf2_sha256.hash(pw, rounds=200000, salt_size=16)

    def check_password(self, pw):
        return pbkdf2_sha256.verify(pw, self.password)
