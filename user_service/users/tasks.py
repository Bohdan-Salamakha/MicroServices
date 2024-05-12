from celery.app import shared_task

from .models import User


@shared_task
def check_user_exists(user_id):
    return bool(User.objects.filter(id=user_id))
