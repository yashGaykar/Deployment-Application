#!/bin/sh
export FLASK_APP=./src/runcelery.py
export FLASK_ENV=development
export FLASK_DEBUG=1
celery -A src.runcelery:celery1 worker -l info --concurrency=2 --pool=threads &
flask run --host=0.0.0.0 --port=5000 
