#!/usr/bin/env python3
"""
Application dependencies related tasks for Invoke.
"""

__version__ = "1.0"

__author__ = "Amit"
__copyright__ = "Copyright (C) 2019 Amit"
__license__ = "Amit"

import os
import logging
from logging import handlers
from invoke import task

from app import settings

# Set up a specific logger with our desired output level
log = logging.getLogger(__name__) # pylint: disable=invalid-name
log.setLevel(logging.INFO)

# Create rotation handler
handler = handlers.RotatingFileHandler( # pylint: disable=invalid-name
    settings.LOG_FILES['tasks'], maxBytes=5*1024*1024, backupCount=5)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter( # pylint: disable=invalid-name
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
log.addHandler(handler)

@task
def install_project_dependencies(context, warn=True):
    """
    Install Python dependencies listed in requirements.txt.
    """
    log.info("Installing project dependencies...")
    context.run("pip install -r {}/requirements.txt ".format(settings.PROJECT_ROOT), warn=warn)
    log.info("Project dependencies are installed.")


@task
def run_pylint(context, warn=True):
    """
    Run pylint on python files.
    """
    log.info("Running pylint...")
    context.run("pylint {}".format(settings.BASE_DIR), warn=warn)
    context.run("pylint {}/tasks".format(settings.PROJECT_ROOT), warn=warn)
    context.run("pylint {}/tests".format(settings.PROJECT_ROOT), warn=warn)
    log.info("Pylint finshed.")


@task
def run_pytest(context, warn=True):
    """
    Run unittest using pytest.
    """
    log.info("Running pytest with coverage tool...")
    context.run(
        "pytest --cov-config={0}/.coveragerc --cov={1} {2}/tests --cov-report html:{3}".format(
            settings.PROJECT_ROOT,
            settings.BASE_DIR,
            settings.PROJECT_ROOT,
            settings.HTML_REPORT,
            ),
        warn=warn
    )
    log.info("Pytest finshed.")


@task
def run_main(context, warn=True):
    """
    Run unittest using pytest.
    """
    log.info("Starting flask and running main.py ...")
    context.run("python {}/main.py".format(settings.BASE_DIR), warn=warn)
    log.info("API Closed.")

@task
def run(context, install=True, warn=True):
    # pylint: disable=unused-argument
    """
    Install project dependencies.
    """
    if install:
        install_project_dependencies(context, warn)

    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if env_flask_config_name is None:
        os.environ['FLASK_CONFIG'] = 'production'
        env_flask_config_name = 'production'

    if env_flask_config_name == 'testing':
        run_pytest(context, warn)
    elif env_flask_config_name == 'development':
        run_pylint(context, warn)
        run_pytest(context, warn)
        run_main(context, warn)
    elif env_flask_config_name != 'production':
        run_main(context, warn)
    else:
        run_main(context, warn)
