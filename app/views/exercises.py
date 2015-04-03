from flask import jsonify, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from app import api, models, db
from app.models import datetime_converter

import datetime

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

        super(ExercisesAPI, self).__init__()

    def get(self):
        """
            Returns exercises that match the query.
            Additional parameters allowed (you can use multiple):

            user_id : int   filter by user id
            type    : str   filter by activity type
            value   : int   filter by average heart rate

        """

        self.reqparse.add_argument('user_id', type=int)
        self.reqparse.add_argument('type', type=str)
        self.reqparse.add_argument('average_hr', type=int, dest='avg_heart_rate')

        args = self.reqparse.parse_args()
        filter_args = dict((k, v) for k, v in args.iteritems() if v)  # remove empty dict items

        exercises = models.Exercise.query.filter_by(**filter_args)    # filter by given args
        
        if exercises:
            return jsonify(exercises=[m.as_dict() for m in exercises])

    def post(self):
        """
            Creates a new exercise with given args. Returns 201 on success.

            user_id     : int   the id of the user exercising
            type        : str   the activity type. i.e. ice hockey
            start       : int   the start time of the exercise (seconds since epoch)
            end         : int   the end time of the exercise (seconds since epoch)

        """

        self.reqparse.add_argument('user_id', type=int, required=True)
        self.reqparse.add_argument('type', type=str, required=True)
        self.reqparse.add_argument('start', type=datetime_converter)
        self.reqparse.add_argument('end', type=datetime_converter)
        #self.reqparse.add_argument('average_hr', type=int, dest='avg_heart_rate') # This should be calculated

        args = self.reqparse.parse_args()

        # convert the end and start times to DateTime objects on creation
        #if "start" in args:
        #    args["start"] = datetime.datetime.fromtimestamp(args["start"])
        #if "end" in args:
        #    args["end"] = datetime.datetime.fromtimestamp(args["end"])

        # TODO: calculate the duration here (?) depending on the startts and endts
        # TODO: calculate the average HR here (?)

        m = models.Exercise(**args)

        db.session.add(m)
        db.session.commit()

        return m.id, 201

# API endpoints
api.add_resource(ExerciseAPI, '/exercises/<int:id>')    # get an exercise by id
api.add_resource(ExercisesAPI, '/exercises/')           # fetch all the exercises