"""
Temporary settings for generating migrations without a PostgreSQL connection.
Uses SQLite instead of PostgreSQL just for the makemigrations command.
"""
from timetracker.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
