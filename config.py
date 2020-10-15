import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
    POSTS_PER_PAGE_API = 10
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    RESOURCE_ID = {
        "afisha": 1,
        "village": 2,
        "vc": 3
    }


