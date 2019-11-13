#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Entry point for api
"""

from app import settings
from app import create_app

def main():
    ''' main function that will run app. '''
    app = create_app(flask_config_name=None)
    app.run(
        host=settings.FLASK_CONF['HOST'],
        port=settings.FLASK_CONF['PORT'],
        debug=settings.FLASK_CONF['DEBUG'],
        use_reloader=True
    )

if __name__ == "__main__":
    main()
