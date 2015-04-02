from flask import Flask, jsonify
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

__all__ = ['make_json_app']


class CustomApi(Api):
    """
    Used to overwrite Api.error_router since it ignores
    programmer-given error message descriptions
    """

    def error_router(self, original_handler, e):
        """
        Calls the original error handler
        """

        return original_handler(e)


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.
    Code from: http://flask.pocoo.org/snippets/83/

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "The requested URL was not found on the server", "status": 404 }
    """

    def make_json_error(ex):
        response = jsonify(message=
                           ex.data['message']
                           if (hasattr(ex, 'data') and ex.data['message'] is not None)
                           else ex.description if hasattr(ex, 'description') else '',
                           status=ex.code)
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = make_json_app(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = CustomApi(app)


from app import models
from app.views import users, measurements, exercises
