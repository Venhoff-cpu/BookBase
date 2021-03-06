"""
Production Settings for Heroku
"""
import dj_database_url
import environ

from Project_BookBase.settings.base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# False if not in os.environ
DEBUG = env('DEBUG')


# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

GOOGLE_BOOKS_API_KEY = env('GOOGLE_BOOKS_API_KEY')
