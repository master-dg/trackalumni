#!/usr/bin/env bash

set -o errexit  # exit on error

# python -m pip install --upgrade pip
# pip install -r requirements.txt
# python manage.py migrate  
# celery -A TrackYourAlumni.celery worker --pool=threads -l INFO
# celery -A TrackYourAlumni beat -l INFO


#!/bin/bash

# Open first terminal and run commands
#!/bin/bash

# Terminal 1
screen -dmS terminal1 bash -c "pip install --upgrade pip; pip install -r requirements.txt; python manage.py migrate"

# Terminal 2
screen -dmS terminal2 bash -c "celery -A TrackYourAlumni.celery worker --pool=threads -l INFO"

# Terminal 3
screen -dmS terminal3 bash -c "celery -A TrackYourAlumni beat -l INFO"