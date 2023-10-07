#!/bin/bash
source venv/bin/activate
flask db upgrade
flask exec create-tables
exec gunicorn -b :5000 --log-level info base_habilis:app
# exec gunicorn -b :5000 --access-logfile - --error-logfile - base_habilis:app