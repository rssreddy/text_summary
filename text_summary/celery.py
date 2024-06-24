# project_root/celery.py
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'text_summary.settings')  # Replace with your project name

app = Celery('text_summary')  # Replace with your project name
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Example of a task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
