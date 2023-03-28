import os
from celery import Celery
from django.conf import settings
from TrackYourAlumni.settings import CELERY_TIMEZONE
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrackYourAlumni.settings')

app = Celery('TrackYourAlumni')
app.conf.enable_utc=False
app.conf.update(timezone=CELERY_TIMEZONE)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')


app.conf.beat_schedule={
    
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

from datetime import timedelta
app.conf.beat_schedule = {
    # Disable cleanup task by scheduling to run every ~1000 years
    'backend_cleanup': {
        'task': 'celery.backend_cleanup',
        'schedule': timedelta(days=365*10),
        'relative': True,
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')