import os

SECRET_KEY = 'random_secret_please_change'

basedir = os.path.abspath(os.path.dirname(__file__))

# for sqlite:
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# for postgresql + postgis:
# SQLALCHEMY_DATABASE_URI = 'postgresql://yourusername:yourpassword@localhost/yournewdb'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:gis@localhost/gisdb' #gis_database
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
