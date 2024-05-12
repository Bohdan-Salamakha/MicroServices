import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_service.settings")

app = Celery("user_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_routes = {
    'user_service.tasks.check_user_exists': {'queue': 'check_user_queue'},
}

app.autodiscover_tasks()
