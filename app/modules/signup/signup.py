#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
This file for creating api.
"""

__version__ = "1.0"

__author__ = "Amit"
__copyright__ = "Copyright (C) 2019 Amit"
__license__ = "Amit"

import logging

from flask import Blueprint
from flask import request
from flask import jsonify

from app import settings
from app.utils import helper

# Set up a specific logger with our desired output level
helper.setup_logger('signup', settings.LOG_FILES['signup'])
log = logging.getLogger('signup')

blueprint = Blueprint('api', __name__)

@blueprint.route('/testapi/', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def test_api():
    """
    This is test function for creating future api.
    """
    log.info("Method %s is called.", request.method)
    if request.method == "POST":
        data = {'POST' : 'POST API SUCCESS !!'}
        return  jsonify(data), 200

    if request.method == "GET":
        data = {'GET' : 'GET API SUCCESS !!'}
        return  jsonify(data), 200

    if request.method == "PUT":
        data = {'PUT' : 'PUT API SUCCESS !!'}
        return  jsonify(data), 200

    if request.method == "PATCH":
        data = {'PATCH' : 'PATCH API SUCCESS !!'}
        return  jsonify(data), 200

    if request.method == "DELETE":
        data = {'DELETE' : 'DELETE API SUCCESS !!'}
        return  jsonify(data), 200

    data = {'UNKNOWN' : 'Unknown request made.'}
    return  jsonify(data), 400
