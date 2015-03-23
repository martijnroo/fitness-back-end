from app import db

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

"""
class HeartBeat(db.Model):
    # heartbeat datamodel here -> foreign key to user
"""