from flask import jsonify, abort
from flask.ext.restful import Api, Resource, reqparse
from app import api, models, db

from config import DEBUG

"""

    The API routing and logic is done here, as an example, I created a
    UserAPI, which works as an API resource serving user information from
    several endpoints, which are defined at the bottom of the file.

    Each API resource may have routes for each type of HTTP request,
    in this case for example, all the users can be queried via the UserAPI
    endpoint /user/<user_id>. (This returns a well-parsed JSON-string of the
    database entries).

    Instead of using pure Flask, we should work with Flask-RESTful, which
    gives us a nice way to work with API endpoints.

    https://flask-restful.readthedocs.org/en/0.3.2/

"""


# API views here
class UserAPI(Resource):
    """
        UserAPI handles basic CRUD for user model:
        create, read, update, delete users in db.
    """

    def __init__(self):

        """
            For each API endpoint, you may add additional arguments,
            which are parsed by the RequestParser. In this case, it could
            be for example the format we want to fetch the data
            or a certain timeframe we want to query the heart
            beat data from.

            For example:
            PUT http://fitnessapp.heroku.com/user/2?name=peter
            to change the name of the user in database.
        """

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True)
        super(UserAPI, self).__init__()

    def get(self, id=-1):
        """
            Returns user info.
        """

        # if id provided, fetch the user from db and return it as json
        u = models.User.query.get(int(id))

        if not u:
            return abort(404)

        return jsonify(u.as_dict())

    def put(self, id):
        """
            Updates the user information
        """
        # Fetch the arguments, in this example case name=Peter
        args = self.reqparse.parse_args()

        # Print them for debugging
        print "ARGUMENTS ------------------"
        print args

        # Fetch the user and update the fields, unless it is not
        # a valid ID, then create it
        u = models.User.query.get(int(id))

        if u:
            # update the SQLAlchemy model
            if args['name']:
                u.nickname = args['name']
            # commit it to the database
            db.session.commit()
            return '', 204
        else:
            # Create new user
            u = models.User(nickname=args['name'], id=int(id))
            db.session.add(u)
            db.session.commit()
            return u.id, 201

    def delete(self, id):
        """
            Deletes the user profile from the database. Return 204 on successful
            deletion.
        """

        u = models.User.query.get(id)
        if u:
            db.session.delete(u)
            db.session.commit()
            return '', 204
        return abort(404)


class UsersAPI(Resource):
    """
        Show all the users in DB
    """

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True)
        super(UsersAPI, self).__init__()

    def get(self):
        users = models.User.query.all()

        if users:
            return jsonify(users=[u.as_dict() for u in users])
        else:
            return jsonify(users=[])

    def post(self):
        """
            Creates a new user with given args. Returns 201 on success.
        """

        args = self.reqparse.parse_args()

        u = models.User(nickname=args['name'])
        db.session.add(u)
        db.session.commit()

        return u.id, 201


class AuthenticationAPI(Resource):
    """
        Handles the user authentication.
        TODO!
    """
    def get(self):
        return {'token': 'X12391239ushda9dajq19qWFQ")#hw2l3ihtw283rhf'}

class Populate(Resource):
    """
        Populates the database
    """
    def get(self):

        from app.models import User, Measurement, Exercise
        import random
        import datetime
        import time

        user_names = ["Pertti", "Tapio", "Jones", "Jack", "Jackson"]
        types = ["jogging", "running", "walking", "sleeping", "longboarding", "ice hockey", "rugby"]
        current_time = int(time.time())

        # create some users
        for idx, name in enumerate(user_names):
            u = models.User(nickname=name, id=idx-1)
            db.session.add(u)

        # create some measurements
        for i in range(0, len(user_names)):
            for j in range(0, 10):
                r = random.randint(30, 140)
                t = datetime.datetime.utcfromtimestamp(current_time - random.randint(0, 43200)) # last 12 hours
                m = models.Measurement(user_id=i, rr_value=r, timestamp=t)
                db.session.add(m)

        # add a few exercises
        for i in range(0, len(user_names)):
            for j in range(0, 3):
                start_time = current_time - random.randint(0, 43200)
                end_time = min((start_time + random.randint(0, 43200)), current_time)
                start = datetime.datetime.utcfromtimestamp(start_time)
                end = datetime.datetime.utcfromtimestamp(end_time)
                e = models.Exercise(user_id=i, start=start, end=end, type=random.choice(types))
                db.session.add(e)

        db.session.commit()

        return "success.", 201

if DEBUG:
    api.add_resource(Populate, '/populate/')

# API endpoints
api.add_resource(UserAPI, '/users/<int:id>')
api.add_resource(UsersAPI, '/users/')
api.add_resource(AuthenticationAPI, '/auth')
