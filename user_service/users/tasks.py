from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import User


@shared_task
def check_user_exists(user_id):
    try:
        User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return False
    else:
        return True
