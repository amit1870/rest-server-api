#!/usr/bin/env python3
# disable too-many-local variable
# pylint: disable=R0914
# disable too-many-branches
# pylint: disable=R0912
# disable too-many-nested-blocks
# pylint: disable=R0101
# disable too-many-return-statements
# pylint: disable=R0911
"""
Util function for app.
"""

__version__ = "1.0"

__author__ = "Amit"
__copyright__ = "Copyright (C) 2019 Amit"
__license__ = "Amit"

import datetime
from collections import namedtuple
import logging
from logging import handlers
import colorlog

from app import settings
from app.utils import datehelper as dt

FIELD_FORMATS = {
    'DATE':'date',
    'DATE_TIME':'date-time',
    'INT32':'int32',
    'INT64':'int64',
    'FLOAT':'float',
    'BINARY':'binary',
    'EMAIL':'email',
}
FIELD_TYPES = {
    'STRING'  :'string',
    'NUMBER'  :'number',
    'INTEGER' :'integer',
    'BOOLEAN' : 'boolean',
    'ARRAY'   : 'array',
    'OBJECT'  : 'object',
}
SKIP_FORMAT = ['int', 'float', 'binary', 'byte', 'files']

DATA_TYPES = {
    'string'  : [
        ('date', 'date-time', 'password', 'email',
         'uri', 'hostname', 'uuid', 'ipv4', 'ipv6'),
        ('pattern')
        ],
    'files'   : [('binary', 'byte')],
    'number'  : [('-', 'float', 'double', 'int32', 'int64'), ('minimum', 'maximum')],
    'integer' : [('-', 'int32', 'int64'), ('minimum', 'maximum')],
    'boolean' : [('true', 'false')],
    'array'   : [('array')],
    'object'  : [()],
}

def iter_prop(prop):
    '''
    An helper to iterate dictionary and convert it dictionary.
    '''
    attibutes = {}
    for attribute_name, value in prop.items():

        attribute_type = attribute_format = attribute_enum = None

        if 'type' in value:
            attribute_type = value['type']
        if 'format' in value:
            if value['format'] in ['int32', 'int64']:
                attribute_format = 'int'
            elif value['format'] in ['float', 'double']:
                attribute_format = 'float'
            else:
                attribute_format = value['format']
        if 'enum' in value:
            attribute_enum = value['enum']

        attibutes[attribute_name] = (attribute_type, attribute_format, attribute_enum)

    return attibutes

def remove_spaces(string_):
    ''' remove space, tabs, newline '''
    try:
        string_ = string_.strip(' \t\n\r')
        if len(string_.split()) > 1:
            string_ = ' '.join(string_.split())
        return string_
    except TypeError:
        return TypeError

def is_empty(string_):
    ''' return True for empty and False for non-empty '''
    try:
        return len(string_) == 0
    except TypeError:
        return TypeError

def is_valid_email(email):
    ''' return True if valid email else False '''
    try:
        space = ' '
        if space in email:
            return False
        import re
        regex = r"[^@]+@[^@]+\.[^@]+"
        return True if re.fullmatch(regex, email) is not None else False
    except TypeError:
        return TypeError

def create_attribute(json_fp, collections):
    """
        :param json_fp: json file.
        :type: file
        :param collections: collection name
        :type: list
        :return: dict of attributes
        :rtype: dict

    """
    import json

    try:
        with open(json_fp, 'r') as jsn:
            try:
                json_obj = json.load(jsn)
            except json.decoder.JSONDecodeError as exc:
                raise exc
            else:
                attributes = {}

                if collections is None:
                    collections = json_obj['definitions'].keys()

                for collection in collections:
                    properties = json_obj['definitions'][collection]['properties']
                    properties_attr = iter_prop(properties)
                    attributes = {**attributes, **properties_attr}

                return attributes

    except FileNotFoundError as exc:
        raise exc

def _clean_data(key, value, field_type=None, field_format=None, field_enum=None):
    error = {}
    if field_type == FIELD_TYPES['STRING']:
        if field_format not in DATA_TYPES['files']:
            if isinstance(value, str) is False:
                error['error'] = "'%s' is not valid string with '%s'." %(key, value)
            else:
                value = remove_spaces(value)

    elif field_type == FIELD_TYPES['INTEGER']:
        if isinstance(value, int) is False:
            error['error'] = "%s is not an integer with '%s'." %(key, value)

    elif field_type == FIELD_TYPES['NUMBER']:
        if field_format is None:
            if isinstance(value, int) is False and isinstance(value, float) is False:
                error['error'] = "%s is not a number with '%s'." %(key, value)
        else:
            if isinstance(value, field_format) is False:
                error['error'] = "%s is not a number with '%s'." %(key, value)

    elif field_type == FIELD_TYPES['BOOLEAN']:
        if value not in ['true', 'false']:
            error['error'] = "%s is not a boolean with '%s'." %(key, value)

    elif field_type == FIELD_TYPES['ARRAY']:
        pass

    elif field_type == FIELD_TYPES['OBJECT']:
        pass

    if field_format == FIELD_FORMATS['DATE']:
        tmp_value = None
        try:
            tmp_value = dt.get_datetime_object(value, '%Y-%m-%d')
        except ValueError:
            error['error'] = "%s has not valid date format with '%s'." %(key, value)
        if isinstance(tmp_value, datetime.date) is False:
            error['error'] = "%s has not valid date format with '%s'." %(key, value)

    elif field_format == FIELD_FORMATS['DATE_TIME']:
        tmp_value = None
        try:
            tmp_value = dt.get_datetime_object(value, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            error['error'] = "%s has not valid date time format with '%s'." %(key, value)
        if isinstance(tmp_value, datetime.datetime) is False:
            error['error'] = "%s has not valid date time format with '%s'." %(key, value)

    elif field_format == FIELD_FORMATS['EMAIL']:
        if not is_valid_email(value):
            error['error'] = "'%s' is not valid email with '%s'." %(key, value)

    if field_enum is not None and value not in field_enum:
        error['error'] = "'%s' is not valid value with '%s'." %(key, value)

    if field_type == FIELD_TYPES['STRING']:
        if is_empty(value):
            error['error'] = "'%s' is not valid string with '%s'." %(key, value)

    return value, error

def mandatory_check(dict_, mandatory):
    '''
    return True if all mandatory fields present
    return False if all mandatory fields not present
    '''
    try:
        for key in mandatory:
            try:
                dict_val = dict_[key]
                if not dict_val:
                    return False
                elif not isinstance(dict_val, int) and dict_val.strip() == '':
                    return False
            except KeyError:
                return False
    except TypeError:
        return False
    return True

def clean_data(cleaning_data, mandatory=None, collections=None):
    """Returns the dict as a model

        Arguments:
            :param cleaning_data: A dict.
            :type: dict
            :param collections: a list of collection
            :type: list
            :return: dictionary of cleaned_data
            :rtype: dict

        Example:
            clean_data(cleaning_data, collections=['Student', 'Employee', 'Attendance'])
            clean_data(cleaning_data, collections=['student'])
            clean_data(cleaning_data, collections=None)
            clean_data(cleaning_data)

    """

    error = {}
    if mandatory is not None and mandatory_check(cleaning_data, mandatory) is False:
        error['error'] = "Mandatory parameter check failed. Please check it."
        return error

    collection_attributes = create_attribute(settings.JSON_FILE_PATH, collections)
    cleaned_data = {}
    for key, value in cleaning_data.items():
        if key in collection_attributes:
            if isinstance(value, list):
                cleaned_data[key] = []
                for row in value:
                    nested_dict = {}
                    for rowkey, rowval in row.items():
                        if rowkey in collection_attributes:
                            field_type, field_format, field_enum = collection_attributes[rowkey]
                            rvalue = rowval
                            if rowval != '':
                                rvalue, error = _clean_data(
                                    rowkey, rowval, field_type, field_format, field_enum
                                )
                                if error:
                                    return error
                            nested_dict[rowkey] = rvalue
                        else:
                            error['error'] = "%s not found in schema." %key
                            return error
                    cleaned_data[key].append(nested_dict)
            elif isinstance(value, dict):
                cleaned_data[key] = {}
                for rowkey, rowval in value.items():
                    if rowkey in collection_attributes:
                        field_type, field_format, field_enum = collection_attributes[rowkey]
                        rvalue = rowval
                        if rowval != '':
                            rvalue, error = _clean_data(
                                rowkey, rowval, field_type, field_format, field_enum
                            )
                            if error:
                                return error
                        cleaned_data[key][rowkey] = rvalue
                    else:
                        error['error'] = "%s not found in schema." %key
                        return error
            else:
                field_type, field_format, field_enum = collection_attributes[key]
                rvalue = value
                if value != '':
                    rvalue, error = _clean_data(
                        key, value, field_type, field_format, field_enum
                    )
                    if error:
                        return error
                cleaned_data[key] = rvalue
        else:
            error['error'] = "%s not found in schema." %key
            return error

    return cleaned_data if not error else error


def setup_logger(logger_name, log_file, level=logging.INFO):
    """
    Create log file and sets its level.
    """

    # Set up a specific logger with our desired output level
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create rotation handler
    handler = handlers.RotatingFileHandler(
        log_file,
        maxBytes=settings.LOG_FILE_SIZE,
        backupCount=5
    )

    handler.setLevel(level)

    # create a logging format
    formatter = colorlog.ColoredFormatter(
        (
            '%(asctime)s '
            '[%(log_color)s%(levelname)s%(reset)s] '
            '[%(cyan)s%(name)s%(reset)s] '
            '%(message_log_color)s%(message)s'
        ),
        reset=True,
        log_colors={
            'DEBUG': 'bold_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'DEBUG': 'white',
                'INFO': 'bold_white',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red',
            },
        },
        style='%'
    )
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

def get_database_settings(selected):
    ''' return tuple of settings from settings'''
    name = settings.DATABASES[selected]['NAME']
    user = settings.DATABASES[selected]['USER']
    password = settings.DATABASES[selected]['PASSWORD']
    host = settings.DATABASES[selected]['HOST']
    database = namedtuple('database', ['name', 'host', 'user', 'passwd'])
    return database(name, host, user, password)
