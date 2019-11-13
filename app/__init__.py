#!/usr/bin/env python3
"""
Entry point to the Flask APP.
"""
import logging
import os
import sys

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
    'local': 'local_config.LocalConfig',
}

def create_app(flask_config_name=None, **kwargs):
    """
    Entry point to the SmartCampus application.
    """
    from flask import Flask
    from flask import current_app

    app = Flask(__name__, **kwargs)
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'local'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                "FLASK_CONFIG environment variable (\"%s\") and flask_config_name argument "
                "(\"%s\") are both set and are not the same." % (
                    env_flask_config_name,
                    flask_config_name
                )
            )

    try:
        app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])
    except ImportError:
        if flask_config_name == 'local':
            with app.app_context():
                current_app.logger.error(
                    "You have to have `local_config.py`. "
                    "Alternatively, you may set `FLASK_CONFIG` "
                    "environment variable to one of the following options: "
                    "development, production, testing."
                )
            sys.exit(1)
        raise

    if app.debug:
        logging.getLogger('main').setLevel(logging.DEBUG)
        with app.app_context():
            current_app.logger.setLevel(logging.DEBUG)

    from . import extensions
    extensions.init_app(app)

    from . import modules
    modules.init_app(app)

    return app
