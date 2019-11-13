#!/usr/bin/env python3
# pylint: disable=missing-docstring
"""
Signup module
============
"""

def init_app(app, **kwargs):
	# pylint: disable=unused-argument,unused-variable
    from app.modules.signup import signup
    app.register_blueprint(signup.blueprint)
