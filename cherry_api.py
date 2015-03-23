import random
import sqlite3
import string
import json

import argparse

import cherrypy

DB_STRING = "fitness.db"


class StringGeneratorWebService(object):
    exposed = True

    def GET(self):
        with sqlite3.connect(DB_STRING) as conn:
            c = conn.cursor()
            c.execute("SELECT value FROM user_string WHERE session_id=?",
                      [cherrypy.session.id])
            result = c.fetchone()
            c.close()
            if result is not None:
                return result[0]
            else:
                raise cherrypy.HTTPError(404, 'This session has not stored any strings yet')

    @cherrypy.tools.accept(media='application/json')
    def POST(self, length=8):
        cherrypy.session['store_session_id'] = 'true'
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        with sqlite3.connect(DB_STRING) as c:
            c.execute("INSERT INTO user_string VALUES (?, ?)",
                      [cherrypy.session.id, some_string])
        return some_string

    def PUT(self, another_string):
        with sqlite3.connect(DB_STRING) as c:
            c.execute("UPDATE user_string SET value=? WHERE session_id=?",
                      [another_string, cherrypy.session.id])

    def DELETE(self):
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM user_string WHERE session_id=?",
                      [cherrypy.session.id])


def setup_database():
    """
    Create the `user_string` table in the database
    on server startup
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE user_string (session_id, value)")


def cleanup_database():
    """
    Destroy the `user_string` table from the database
    on server shutdown.
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE user_string")


def jsonify_error(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': status, 'message': message})


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.json_out.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), # for using HTTP requests (GET, POST,..)
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
            'error_page.default': jsonify_error,
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)

    parser = argparse.ArgumentParser(description='Run the Fitness API.')
    parser.add_argument('--local', dest='local', action='store_const',
                       const=True, default=False,
                   help='listen on localhost')
    args = parser.parse_args()
    if not args.local:
        cherrypy.server.socket_host = '172.31.2.6'
        cherrypy.server.socket_port = 8080

    webapp = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)


