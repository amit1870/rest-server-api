#!/usr/bin/env python3
# pylint: disable=invalid-name,redefined-outer-name
''' Fixture '''

import pytest
from app import create_app

@pytest.fixture
def flask_app():
    """
    dummy
    """
    app = create_app(flask_config_name='development')
    yield app

@pytest.fixture
def client(flask_app):
    """
    A test client for the app.
    """
    return flask_app.test_client()
