#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Test cases for app.
"""

def test_get(client):
    '''testing endpoint /testapi for GET'''
    assert client.get("/testapi/").status_code == 200

def test_port(client):
    '''testing endpoint /testapi for GET'''
    assert client.get("/testapi/").status_code == 200
