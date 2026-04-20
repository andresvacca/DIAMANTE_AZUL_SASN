import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diamante_azul.settings')

app = Celery('diamante_azul')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()