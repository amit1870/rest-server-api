#!/usr/bin/env python3
# disable too-many-local variable
# pylint: disable=R0914
# disable too-many-branches
# pylint: disable=R0912
# disable too-many-nested-blocks
# pylint: disable=R0101
# pylint: disable invalid-name

"""
This module contains functions for generating id for
Student(ST), Parent(PT), Employee(EM), Visitor(VT).
"""

__version__ = "1.0"

__author__ = "Abhishek Sinha"
__copyright__ = "Copyright (C) 2019 Amit"
__license__ = "Amit"

from app import settings
from app.utils import database as db
from app.utils import datehelper as dt
from app.utils import helper

def _create_collection(cursor, name):
    """
    Create collection with some predefined values.
    """

    collection = cursor[name]
    student = {
        'type': "student",
        'data': {'idtype':'10', 'year':'2019', 'idval':'000000'}
    }
    parent = {
        'type': "parent",
        'data':{'idtype':'30', 'year':'2019', 'idval':'000000'}
    }
    employee = {
        'type': "employee",
        'data': {'idtype':'40', 'year':'2019', 'idval':'000000'}
    }
    visitor = {
        'type': "visitor",
        'data': {'idtype':'50', 'year':'2019', 'idval':'000000'}
    }
    collection.insert_many([student, parent, employee, visitor])

    return collection


def _get_campus_id():
    """
    TODO: How Campus ID will be taken need to be written
    This function is used to get the Campus ID
    Parameters: NA
    Returns:
    string: campus_id
    """
    campus_id = 1000
    return str(campus_id)

def _generate(idtype):
    """
    This function is used for for function generate_id()
    """
    ID_TYPES = { # pylint: disable=invalid-name
        'ST' : ('student', '10', '29'),
        'PT' : ('parent', '30', '39'),
        'EM' : ('employee', '40', '49'),
        'VT' : ('visitor', '50', '99'),
    }
    database = helper.get_database_settings('production')
    cursor, exception = db.create_connection(
        user=database.user,
        passwd=database.passwd,
        host=database.host,
        db_name=database.name)
    if exception:
        raise exception

    collection_name = settings.COLLECTIONS['GENERATE_ID']
    if collection_name not in cursor.list_collection_names():
        collection_cursor = _create_collection(cursor, collection_name)
    else:
        collection_cursor = cursor[collection_name]


    query = {"type": ID_TYPES[idtype][0]}
    filter_ = {"_id": 0, "data": 1}
    doc = collection_cursor.find(query, filter_)

    received_doc = doc[0]['data']

    current_year = dt.get_current_year()
    current_year = str(current_year)
    current_campus_id = _get_campus_id()
    current_id_type = ID_TYPES[idtype][1]
    current_id_val = f"{1:06}" # 000 001

    if current_year == received_doc['year']: #If curent year is same as received year
        if received_doc['idval'] == '999999': # If received idval = 999 999

            if received_doc['idtype'] == ID_TYPES[idtype][2]:
                current_id_type = ID_TYPES[idtype][1]
                current_id_val = f"{1:06}" # 000 001
            else:
                current_id_type = str(int(received_doc['idtype']) + 1)
                current_id_val = f"{1:06}" # 000 001
        else:
            current_id_val = f"{int(received_doc['idval']) + 1 :06}"
    elif current_year < received_doc['year']:
        return "ERROR"

    generated_id = ''.join([current_campus_id, current_id_type, current_year, current_id_val])
    update_doc = {'idtype': current_id_type, 'year': current_year, 'idval': current_id_val}

    # Update the generated_id in collection
    received_doc = {"data":received_doc}
    update_doc = {"$set":{"data": update_doc}}
    collection_cursor.update_one(received_doc, update_doc)
    collection_cursor.close()
    cursor.close() # pylint: disable=E1101

    return int(generated_id)

def generate_id(idtype):
    """
    This function is used to generate ID for
    Student, Parent, Employee and Visitor.
    Arguments:
        :param idtype: A string.
        :type: string
        :return: id
        :rtype: int

    Example:
        generate_id('ST')
        generate_id('PT')
        generate_id('EM')
        generate_id('VT')
    """

    return _generate(idtype)
