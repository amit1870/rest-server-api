#!/bin/sh
echo "starting script!"

export PYTHONPATH=/home/cxedu/smartcampus
echo "python path location: $PYTHONPATH"

export FLASK_CONFIG=production
echo "flask config: $FLASK_CONFIG" 

python3 app/main.py
