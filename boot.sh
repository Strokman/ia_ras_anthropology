#!/bin/bash
source venv/bin/activate
flask db upgrade
flask exec create-tables
exec gunicorn -w 2 -b :5000 --access-logfile - --error-logfile - base_habilis:app