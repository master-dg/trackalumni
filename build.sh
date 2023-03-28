#!/usr/bin/env bash

set -o errexit  # exit on error

# python -m pip install --upgrade pip
# pip install -r requirements.txt
# python manage.py migrate  
# celery -A TrackYourAlumni.celery worker --pool=threads -l INFO
# celery -A TrackYourAlumni beat -l INFO


#!/bin/bash

# Open first terminal and run commands
gnome-terminal --tab --title="Terminal 1" --command="bash -c 'echo Running commands in Terminal 1...; \
python -m pip install --upgrade pip; \
pip install -r requirements.txt; \
python manage.py migrate; \
exec bash'"

# Open second terminal and run command
gnome-terminal --tab --title="Terminal 2" --command="bash -c 'echo Running commands in Terminal 2...; \
celery -A TrackYourAlumni.celery worker --pool=threads -l INFO; \
exec bash'"

# Open third terminal and run command
gnome-terminal --tab --title="Terminal 3" --command="bash -c 'echo Running commands in Terminal 3...; \
celery -A TrackYourAlumni beat -l INFO; \
exec bash'"