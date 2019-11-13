# pylint: disable=invalid-name,wrong-import-position
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""


from flask_cors import CORS
cross_origin_resource_sharing = CORS()

def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
            cross_origin_resource_sharing,
    ):
        extension.init_app(app)
