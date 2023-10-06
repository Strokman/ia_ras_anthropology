#!/bin/bash
source venv/bin/activate
flask db upgrade
flask exec create-tables
exec gunicorn -b :5000 --access-logfile - --error-logfile - --log-level=info --capture-output --enable-stdio-inheritance base_habilis:app