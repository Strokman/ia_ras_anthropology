#!/bin/bash
source venv/bin/activate
mkdir logs
flask db upgrade
flask exec create-tables
exec gunicorn -b :5000 --access-logfile - --error-logfile - base_habilis:app