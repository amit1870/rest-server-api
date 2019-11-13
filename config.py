# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os


class BaseConfig(object):
    SECRET_KEY = 'this-really-needs-to-be-changed'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    ERROR_404_HELP = False

    AUTHORIZATIONS = {
        'oauth2_password': {
            'type': 'oauth2',
            'flow': 'password',
            'scopes': {},
            'tokenUrl': '/auth/oauth2/token',
        },
    }

    ENABLED_MODULES = (
        'signup',
    )

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
    CSRF_ENABLED = True


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('CLOUDSML_API_SERVER_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('CLOUDSML_API_SERVER_SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
