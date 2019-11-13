#!/usr/bin/env python3
"""
Database API using pymongo
"""

from urllib.parse import quote_plus

import psycopg2 as gre

from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError,
    OperationFailure)

def create_connection(user, passwd, host='127.0.0.1', port=27017, db_name='smartcampus'):
    """
    Return cursor.
    """
    if user is not None and passwd is not None:
        user = quote_plus(user)
        passwd = quote_plus(passwd)
        exception = None
        cursor = MongoClient(
            host=host,
            port=port,
            username=user,
            password=passwd,
            authSource=db_name,
            authMechanism='SCRAM-SHA-1',
            serverSelectionTimeoutMS=5000
            )
        try:
            cursor.db_name.command('ismaster')
        except (
                ConnectionFailure,
                ServerSelectionTimeoutError,
                OperationFailure) as exc:
            exception = exc
        return cursor[db_name], exception if db_name else cursor, exception

    return "Invalid User and Password provided."


def create_connection_with_postgres(
        user,
        passwd,
        hostaddr='127.0.0.1',
        port='5432',
        db_name='smartcampus'):
    """
    Return connection when successfully connected.
    """
    if user is not None and passwd is not None:
        user = quote_plus(user)
        passwd = quote_plus(passwd)
        exception = None
        try:
            connection = gre.connect(
                database=db_name,
                hostaddr=hostaddr,
                port=port,
                username=user,
                password=passwd)
        except (
                gre.OperationalError,
            ) as exc:
            exception = exc
        return connection, exception

    return "Invalid User and Password provided."
