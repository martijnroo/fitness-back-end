from app import db
from sqlalchemy.schema import ForeignKey
import datetime

"""
    Models.py is the place to store the database schema, which uses SQLAlchemy
    ORM to do the nasty SQL behind the scenes.

    According to the fitness app model, we might want to modify this models
    file to save the heartbeat data in a clever way for each user.
"""

datetime_format = '%Y%m%d%H%M%S%f'


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
    rr_value = db.Column(db.Integer, index=True, nullable=False)

    def __repr__(self):
        return '<Measurement %i>' % (self.id)

    # for json serialization
    def as_dict(self):
        result_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result_dict['timestamp'] = result_dict['timestamp'].strftime(datetime_format)[:17]
        return result_dict


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    start = db.Column(db.DateTime, index=True)
    end = db.Column(db.DateTime, index=True)
    type = db.Column(db.String(64), index=True)
    avg_rr_value = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Exercise %r>' % (self.id)

    # for json serialization
    def as_dict(self):
        result_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result_dict['type'] = result_dict['type'].__str__()
        return result_dict


def datetime_converter(dt_string):
    """
    Helper function for request parsers to convert a datetime string
    to a datetime object.

    :param dt_string: A datetime string in the format yyyymmddhhmmssfff
    :return: Returns a datetime object
    """
    if isinstance(dt_string, int):
        dt_string = str(dt_string)
    if not len(dt_string) is 17:
        raise ValueError('DateTime string needs to be in the format yyyymmddhhmmssfff (17 digits). '
                         '{} is not a valid DateTime'.format(dt_string))

    dt = datetime.datetime.strptime(dt_string, datetime_format)
    return dt


def measurements_list(value):
    """
    A measurement_list type function that validates if all objects
    in the given list have the properties required for a measurement.
    Unrecognized properties of the objects (if present) are ignored.

    :raises ValueError: If any item is not a valid measurement
    :param value: A list of objects
    :return: A list of valid measurements
    """
    measurements = value
    if not isinstance(measurements, list):
        raise ValueError("measurements is not a list")

    result = []
    for measurement in measurements:
        m = dict()

        if 'user_id' not in measurement or not isinstance(measurement['user_id'], int):
            raise ValueError("Measurement without valid user_id in list")
        m['user_id'] = measurement['user_id']

        if 'rr_value' not in measurement or not isinstance(measurement['rr_value'], int):
            raise ValueError("Measurement without valid rr_value in list")
        m['rr_value'] = measurement['rr_value']

        if 'timestamp' in measurement:
            m['timestamp'] = datetime_converter(measurement['timestamp'])

        result.append(m)

    return result
