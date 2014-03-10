import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'temp secret key'
SQLALCHEMY_DATABASE_URI = "postgresql://arsdale:gksehrjs0710@localhost/beauty"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')