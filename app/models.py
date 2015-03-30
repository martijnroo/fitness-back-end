from app import db
from sqlalchemy.schema import ForeignKey
import datetime

"""
    Models.py is the place to store the database schema, which uses SQLAlchemy
    ORM to do the nasty SQL behind the scenes.

    According to the fitness app model, we might want to modify this models
    file to save the heartbeat data in a clever way for each user.
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nickname = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    # for json serialization
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    heart_rate = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Measurement %i>' % (self.id)

    # for json serialization
    def as_dict(self):
        result_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result_dict['timestamp'] = result_dict['timestamp'].__str__()
        return result_dict

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    start_ts = db.Column(db.Integer, index=True)
    end_ts = db.Column(db.Integer, index=True)
    type = db.Column(db.String(64), index=True)
    duration = db.Column(db.Integer, index=True)
    avg_hr = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Exercise %i>' % (self.id)

    # for json serialization
    def as_dict(self):
        result_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result_dict['type'] = result_dict['type'].__str__()
        return result_dict