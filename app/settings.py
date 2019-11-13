#!/usr/bin/env python3
# pylint: disable=too-few-public-methods,invalid-name,missing-docstring,bad-whitespace

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(PROJECT_ROOT, 'data')


# app configuration host, port, debug
FLASK_CONF = {
    'HOST': '0.0.0.0',
    'PORT': 41412,
    'DEBUG': False
}

# Database
DATABASES = {
    'staging': {
        'ENGINE': '',
        'NAME': 'smartcampus',
        'USER': 'proxouser',
        'PASSWORD': 'adminux',
        'HOST': '172.30.76.211',
    },
    'production': {
        'ENGINE': '',
        'NAME': 'cxeducation_deployment',
        'USER': 'proxouser',
        'PASSWORD': 'adminux',
        'HOST': '172.30.76.205'
    }
}

# name of collections for smartcampus database
COLLECTIONS = {
    'GENERATE_ID' : 'idgeneration',
    'EMPLOYEE_ID' : 'empdetails'
}

# openapi.json
JSON_FILE_PATH = os.path.join(DATA_DIR, 'openapi.json')

# log file size in MB
LOG_FILE_SIZE = 10*1024*1024

# log files specific to modules
# Only one log files allowed to one modules
LOG_FILES = {
    'main' : 'main.log',
    'signup' : 'signup.log',
    'tasks' : 'tasks.log',
}

# html report path
HTML_REPORT = os.path.join(PROJECT_ROOT, 'htmlcoverage')
