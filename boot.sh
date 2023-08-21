#!/bin/bash
source venv/bin/activate
flask db upgrade
flask exec create-tables
exec gunicorn -b :5100 --access-logfile - --error-logfile - base_habilis:app