from flask import jsonify, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
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
class ExerciseAPI(Resource):
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
            Returns data for the specific EXERCISE.
			TODO: Implement functionality to return all EXERCISE IDs for a given USER
        """

        # if id provided, fetch the exercise from db and return it as json
        m = models.Exercise.query.get(int(id))

        if not m:
            return abort(404)

        return jsonify(m.as_dict())

    def delete(self, id):
        """
            Deletes the exercise from the database. Return 204 on successful
            deletion.
        """

        m = models.Exercise.query.get(id)
        if m:
            db.session.delete(m)
            db.session.commit()
            return '', 204
        return abort(404)

class ExercisesAPI(Resource):
    """
    """

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int)
        self.reqparse.add_argument('type', type=str)
        self.reqparse.add_argument('startts', type=int)
        self.reqparse.add_argument('endts', type=int)
        self.reqparse.add_argument('duration', type=int)
        self.reqparse.add_argument('value', type=int)
        super(ExercisesAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        # this defines the additional parameters you can filter the query with
        allowed_fields = {
                'user_id': fields.Integer,
                'type': fields.String,
                #'startts': fields.DateTime(attribute='start'),
                #'endts': fields.DateTime(attribute='end'),
                #'duration': fields.Integer,
                'value': fields.Integer(attribute='avg_heart_rate')
        }
        
        filter_args = marshal(args, allowed_fields)                   # filter the allowed_fields from args
        filter_args = dict((k, v) for k, v in args.iteritems() if v)  # remove empty dict items

        print filter_args

        exercises = models.Exercise.query.filter_by(**filter_args)    # filter by given args
        
        if exercises:
            return jsonify(exercises=[m.as_dict() for m in exercises])

    def post(self):
        """
            Creates a new exercise with given args. Returns 201 on success.
        """

        # TODO: calculate the duration here depending on the startts and endts

        args = self.reqparse.parse_args()
        print args

        if not (args['user_id'] and args['type'] and args['startts'] and args['endts'] and args['duration'] and args['value']):
            response = jsonify({'message': 'All fields are required...', 'status': 400})
            response.status_code = 400
            return response

        m = models.Exercise()
        m.user_id = args['user_id'] # No check if user exists!
        m.type = args['type']
        m.start_ts = args['startts']
        m.end_ts = args['endts']
        m.duration = args['duration']
        m.avg_hr = args['value']

        db.session.add(m)
        db.session.commit()

        return m.id, 201

# API endpoints
api.add_resource(ExerciseAPI, '/exercises/<int:id>')
api.add_resource(ExercisesAPI, '/exercises/')