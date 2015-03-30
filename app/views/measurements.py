from flask import jsonify, abort
from flask.ext.restful import Api, Resource, reqparse
from app import api, models, db


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
        m = models.Measurement.query.get(int(id))

        if not m:
            return abort(404)

        return jsonify(m.as_dict())

    def delete(self, id):
        """
            Deletes the user profile from the database. Return 204 on successful
            deletion.
        """

        m = models.Measurement.query.get(id)
        if m:
            db.session.delete(m)
            db.session.commit()
            return '', 204
        return abort(404)

class MeasurementsAPI(Resource):
    """
    """

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int)
        self.reqparse.add_argument('value', type=int)
        super(MeasurementsAPI, self).__init__()

    def get(self):
        measurements = models.Measurement.query.all()

        if measurements:
            return jsonify(measurements=[m.as_dict() for m in measurements])

    def post(self):
        """
            Creates a new user with given args. Returns 201 on success.
        """

        args = self.reqparse.parse_args()
        print args

        if not (args['user_id'] and args['value']):
            response = jsonify({'message': 'The fields user_id and value are both required fields.', 'status': 400})
            response.status_code = 400
            return response

        m = models.Measurement()
        m.user_id = args['user_id'] # No check currently on existence user!
        m.heart_rate = args['value']

        db.session.add(m)
        db.session.commit()

        return m.id, 201


# API endpoints
api.add_resource(MeasurementAPI, '/measurements/<int:id>')
api.add_resource(MeasurementsAPI, '/measurements/')