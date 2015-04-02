from flask import jsonify, abort
from flask_restful import Resource, reqparse
from app import api, db
from sqlalchemy import desc

from app.models import Measurement, datetime_converter

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
class MeasurementAPI(Resource):
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

    def get(self, id=-1):
        """
            Returns user info.
        """

        # if id provided, fetch the user from db and return it as json
        m = Measurement.query.get(int(id))

        if not m:
            return abort(404, "Measurement with given ID not found")

        return jsonify(m.as_dict())

    def delete(self, id):
        """
            Deletes the user profile from the database. Return 204 on successful
            deletion.
        """

        m = Measurement.query.get(id)
        if m:
            db.session.delete(m)
            db.session.commit()
            return '', 204
        return abort(404, "Measurement with given ID not found")


class MeasurementsAPI(Resource):
    """
    """

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, required=True)
        self.reqparse.add_argument('heart_rate', type=int, required=True)

        self.getparser = reqparse.RequestParser()
        self.getparser.add_argument('user_id', type=int)
        self.getparser.add_argument('max', type=int)
        self.getparser.add_argument('from', type=datetime_converter)
        self.getparser.add_argument('until', type=datetime_converter)

        super(MeasurementsAPI, self).__init__()

    def get(self):
        args = self.getparser.parse_args()
        query = Measurement.query.order_by(desc(Measurement.timestamp))
        if args['user_id']:
            query = query.filter(Measurement.user_id == args['user_id'])
        if args['max']:
            query = query.limit(args['max'])
        if args['from']:
            query = query.filter(Measurement.timestamp >= args['from'])
        if args['until']:
            query = query.filter(Measurement.timestamp <= args['until'])

        measurements = query.all()

        if measurements:
            return jsonify(measurements=[m.as_dict() for m in measurements])
        else:
            return jsonify(measurements=[])

    def post(self):
        """
            Creates a new measurement with given args. Returns 201 on success.
        """

        args = self.reqparse.parse_args()

        m = Measurement()
        m.user_id = args['user_id']  # sqlite does not check if user exists in DB!
        m.heart_rate = args['heart_rate']

        db.session.add(m)
        db.session.commit()

        return m.id, 201


# API endpoints
api.add_resource(MeasurementAPI, '/measurements/<int:id>')
api.add_resource(MeasurementsAPI, '/measurements/')