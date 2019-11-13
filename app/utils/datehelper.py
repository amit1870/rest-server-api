#!/usr/bin/env python3
"""
Date utility
"""

import datetime

def get_current_year():
    ''' return current year '''
    now = datetime.datetime.now()
    return now.year

def get_datetime_object(date_string, format_='%Y-%m-%d %H:%M:%S'):
    ''' convert datetime string and return object '''
    return datetime.datetime.strptime(date_string, format_)

def get_datetime_string(date_object, format_='%Y-%m-%dT%H:%M:%S'):
    ''' convert datetime object and return string '''
    return date_object.strftime(format_)
