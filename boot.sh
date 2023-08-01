#!/bin/bash
source venv/bin/activate
flask db upgrade
venv/bin/python create_tables.py
exec gunicorn -b :5100 --access-logfile - --error-logfile - base_habilis:app