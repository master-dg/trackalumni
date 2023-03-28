start cmd /k venv\Scripts\activate & python manage.py runserv   
start cmd /k celery -A TrackYourAlumni.celery worker --pool=threads -l INFO
start cmd /k celery -A TrackYourAlumni beat -l INFO


@echo off
start cmd /k python manage.py runserver
start /B cmd /c "celery -A TrackYourAlumni.celery worker --pool=threads -l INFO" > celery.log 2>&1
start /B cmd /c "celery -A TrackYourAlumni beat -l INFO" > celery_beat.log 2>&1